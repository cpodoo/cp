# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    category = fields.Selection([
        ('PPS', 'PPS'),
        ('RCEL', 'RCEL')
    ], string='Category')
    proposal_date = fields.Date(string='Proposal Date', default=fields.Date.context_today)
    mou_date = fields.Date(string='MoU Date')
    mou_id = fields.Char(string='MoU ID', required=True, copy=False, readonly=True, default='New')
    business_proposal_id = fields.Char(string='Business Proposal ID', required=True, copy=False, readonly=True, default='New')
    about_company = fields.Text(string="About Company")

    custom_order_line_ids = fields.One2many(
        'crm.sale.order.line',
        'lead_id',
        string="Order Lines"
    )

    deliverable_ids = fields.One2many(
        'crm.lead.deliverable',
        'lead_id',
        string='Deliverables'
    )

    installment_ids = fields.One2many(
        'proposal.installment',
        'lead_id',
        string='Payment Installments'
    )
    stage_name = fields.Char(related='stage_id.name')
    stage_sequence = fields.Integer(
        related='stage_id.sequence',
        store=True,
        string="Stage Sequence")

    # COMMERCIALS
    no_of_students = fields.Integer(string='No. of Students')
    first_year_charges = fields.Float(string='First Year Charges')
    second_year_increase = fields.Float(string='Second Year % Increase')
    commercials_terms = fields.Text(string='Commercial Terms')
    agreement_tenure = fields.Integer(string='Agreement Tenure')
    period_type = fields.Selection([
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ], string='Period Type', default='yearly')
    period_month = fields.Integer(string="Monthly")
    period_year = fields.Integer(string="Yearly")
    grade = fields.Selection([
        ('3', '3rd Grade'),
        ('4', '4th Grade'),
        ('5', '5th Grade'),
        ('6', '6th Grade'),
        ('7', '7th Grade'),
        ('8', '8th Grade'),
    ], string='Grade')
    setup_date = fields.Text(string='Setup Date')
    lead_generation_person_id = fields.Many2one('res.users', string='Lead Generation Person')

    invoice_bill_ids = fields.One2many(
        'account.move',
        'opportunity_id',
        domain=[('move_type', '=', 'out_invoice')],
        string="Invoice"
    )

    invoice_bill_count = fields.Integer(
        string="Invoice Count",
        compute='_compute_invoice_count'
    )

    @api.depends('invoice_bill_ids')
    def _compute_invoice_count(self):
        for lead in self:
            lead.invoice_bill_count = len(lead.invoice_bill_ids)

    def action_open_invoice_bills(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.invoice_bill_ids.ids)],
            'context': {'default_move_type': 'out_invoice'},
        }

    def button_generate_a_pdf(self):
        if self.business_proposal_id == ("New"):
            self.business_proposal_id = self.env['ir.sequence'].next_by_code(
                'proposal.bp') or _("New")
            self.proposal_date = fields.Date.today()
        return self.env.ref('custom_crm_proposal.report_business_proposal_action').report_action(self)

    def button_generate_mou_pdf(self):
        if self.mou_id == ("New"):
            self.mou_id = self.env['ir.sequence'].next_by_code(
                'proposal.mou') or _("New")
            self.mou_date = fields.Date.today()
        return self.env.ref('custom_crm_proposal.report_mou_proposal_action').report_action(self)

    def action_mark_won(self):
        res = super().action_mark_won()
        self._create_sales_order_from_lines()
        return res

    def _create_sales_order_from_lines(self):
        for lead in self:
            if lead.custom_order_line_ids:
                order = self.env['sale.order'].create({
                    'partner_id': lead.partner_id.id,
                    'opportunity_id': lead.id,
                })
                # SALE ORDER line
                for line in lead.custom_order_line_ids:
                    self.env['sale.order.line'].create({
                        'order_id': order.id,
                        'product_id': line.product_id.id,
                        'name': line.name,
                        'product_uom_qty': line.product_uom_qty,
                        'price_unit': line.price_unit,
                        'tax_id': [(6, 0, line.tax_ids.ids)],
                    })
                # # DELIVERed line
                # for line in lead.deliverable_ids:
                #     self.env['sale.order.line'].create({
                #         'order_id': order.id,
                #         'product_id': line.item.id,
                #         'name': line.description,
                #         'product_uom_qty': line.quantity,
                #         'product_uom': line.uom.id,
                #         'price_unit': line.price_unit,
                #         'tax_id': [(6, 0, line.tax_ids.ids)],
                #     })

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('mou_id', _("New")) == _("New"):
                vals['mou_id'] = self.env['ir.sequence'].next_by_code(
                    'proposal.mou') or _("New")
            if vals.get('business_proposal_id', _("New")) == _("New"):
                vals['business_proposal_id'] = self.env['ir.sequence'].next_by_code(
                    'proposal.bp') or _("New")
        return super().create(vals_list)

    def create_action_invoice(self):
        self.ensure_one()
        partner = self.partner_id
        if not partner:
            raise UserError("No customer assigned to this opportunity.")

        # Get un-invoiced installments
        pending_lines = self.installment_ids.filtered(lambda l: l.display and not l.is_invoice)
        if not pending_lines:
            raise UserError("No pending installments to invoice.")

        product = self.env['product.product'].search([('name', '=', 'Installment Payment')], limit=1)
        if not product:
            raise UserError("Product 'Installment Payment' not found.")

        invoice_lines = []
        for line in pending_lines:
            invoice_lines.append((0, 0, {
                'name': f'Installment {line.installment_no or ""} - {line.year or ""}',
                'quantity': 1,
                'price_unit': line.amount,
                'product_id': product.id,
                'account_id': product.property_account_income_id.id or product.categ_id.property_account_income_categ_id.id,
            }))
            line.is_invoice = True

        move_vals = {
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': invoice_lines,
            'currency_id': self.company_currency.id,
            'company_id': self.company_id.id,
            'opportunity_id': self.id,
            'ref': self.name,
        }

        invoice = self.env['account.move'].sudo().create(move_vals)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
        }
