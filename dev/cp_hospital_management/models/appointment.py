# -*- coding: utf-8 -*-

from odoo import models, fields, api, _ 
import time
from odoo.exceptions import UserError


class TestType(models.Model):
    _name = "medical.test_type"
    _description = "Type of Lab test"

    name = fields.Char('Test', size=128, help="Test type, eg X-Ray, hemogram,biopsy...", required=True, )

    code = fields.Char('Code', size=128, help="Short name - code for the test", required=True,
                       )
    info = fields.Text('Description')
    product_id = fields.Many2one('product.product', 'Service', required=True)

class MedicalLabAppointment(models.Model):
    _name = "appointment"
    _inherit = ['custom.invoice', 'mail.thread', 'mail.activity.mixin']
    _order = "appointment_sdate desc"

    doctor = fields.Many2one('hr.employee', 'Physician', help="Physician's Name", required=True, )
    name = fields.Char('Appointment ID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    patient = fields.Many2one('res.partner', 'Patient', help="Patient Name", required=True, )
    appointment_sdate = fields.Date('Appointment Start', required=True, default=fields.Datetime.now)
    appointment_edate = fields.Date('Appointment End', required=True, default=fields.Datetime.now)
    request_date = fields.Date('Request Date', required=True, default=fields.Date.context_today)
    urgency = fields.Selection([('Normal', 'Normal'), ('Urgent', 'Urgent'), ('Medical Emergency', 'Medical Emergency')], string='Urgency Level', default='Normal')
    comments = fields.Text('Comments')
    user_id = fields.Many2one('res.users', 'User', help="Login User")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('outcome', 'Outcome'), 
        ('invoiced', 'Invoiced'),
        ('cancel', 'Cancelled',)], string='Status', readonly=True, default='draft', copy=False, tracking=True)

    test_ids = fields.Many2many('medical.test_type', 'apt_test_rel', 'apt_id', 'test_id', string='Tests', required=True, )
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')
    invoice_id = fields.Many2one('account.move',
        string='Invoice',
        copy=False,
        readonly=True)

    invoice_count = fields.Integer(
        compute='_compute_invoice_count',
        string='# of Invoices',
        copy=False,
        default=0
    )
    no_invoice = fields.Boolean('Invoice Exempt', default=False, help="Check this box if the appointment should not be invoiced.")

    @api.depends('invoice_id') 
    def _compute_invoice_count(self):
        for appt in self:
            appt.invoice_count = 1 if appt.invoice_id else 0
 
    def cancel(self):
        self.write({'state': 'cancel'}) 

    def requested(self):
        self.write({'state': 'requested'})

    def outcome(self):
        self.write({'state': 'outcome'})
   
    def _prepare_invoice_line(self, invoice_id):
        lines_vals = []
        for test in self.test_ids:
            if not test.product_id:
                 raise UserError(_("The Test Type '%s' does not have an associated Service Product.") % test.name)

            product = test.product_id
            account_id = product.property_account_income_id.id or product.categ_id.property_account_income_categ_id.id
            if not account_id:
                raise UserError(
                    _('Please define an income account for the product "%s" (or its category).') % (product.name)
                )
            # price = product.lst_price 
            if self.pricelist_id:
                price = self.pricelist_id._get_product_price(product, 1.0, self.patient)
            else:
                price = product.lst_price

            vals = {
                'move_id': invoice_id,
                'product_id': product.id,
                'name': f"{_('Appointment Test')}: {test.name} ({self.name})", 
                'quantity': 1, 
                'price_unit': price,
                'account_id': account_id,
                
            }
            lines_vals.append((0, 0, vals)) 
        return lines_vals
   
    def create_invoices(self):
        if not self:
            return False

        invoice_vals_list = []
        appointments_to_invoice = self 

        for appt in appointments_to_invoice:
            if appt.state != 'outcome':
                raise UserError(_("You can only invoice appointments that are in the 'Outcome' state. Appointment: %s") % appt.name)
            if appt.invoice_id:
                raise UserError(_("Appointment %s is already linked to invoice %s.") % (appt.name, appt.invoice_id.name))
            if appt.no_invoice:
                raise UserError(_("Appointment %s is marked as 'Invoice Exempt'.") % appt.name)
            if not appt.patient:
                 raise UserError(_("Cannot create invoice for appointment %s: Patient is not set.") % appt.name)
            if not appt.test_ids:
                 raise UserError(_("Cannot create invoice for appointment %s: No tests are selected.") % appt.name)

            journal = self.env['account.journal'].search([
                ('type', '=', 'sale'),
                ('company_id', '=', appt.env.company.id)], limit=1)
            if not journal:
                raise UserError(_('Please define a Sales Journal for the company "%s".') % (appt.env.company.name))

            invoice_line_vals = appt._prepare_invoice_line(False)

            invoice_vals = {
                'ref': appt.name, 
                'move_type': 'out_invoice', 
                'narration': f"Invoice for Appointment {appt.name}",
                'partner_id': appt.patient.id,
                'invoice_date': fields.Date.context_today(self),
                'invoice_origin': appt.name,
                'journal_id': journal.id,
                'company_id': appt.env.company.id,
                'invoice_line_ids': invoice_line_vals, 
            }
            invoice_vals_list.append(invoice_vals)

        if not invoice_vals_list:
            return True 
        try:
            moves = self.env['account.move'].with_context(default_move_type='out_invoice').create(invoice_vals_list)
        except Exception as e:
             raise UserError(_("Failed to create invoices. Error: %s") % str(e))
        for appt, move in zip(appointments_to_invoice, moves):
            appt.write({
                'invoice_id': move.id, 
                'state': 'invoiced'
            })

        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        if len(moves) == 1:
            action['view_mode'] = 'form'
            action['res_id'] = moves.id
            action['views'] = [(view_id, view_type) for view_id, view_type in action.get('views', []) if view_type == 'form'] 
            action.pop('domain', None) 
        else:
            action['domain'] = [('id', 'in', moves.ids)]
            action['view_mode'] = 'tree,form' 

        return action

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('appointment') or _('New Appointment')
        return super().create(vals_list)

    def action_view_invoice(self):
        self.ensure_one()
        if not self.invoice_id:
             invoices = self.env['account.move'].search([
                 ('invoice_origin', '=', self.name),
                 ('move_type', '=', 'out_invoice'),
                 ('partner_id', '=', self.patient.id)
             ])
             if len(invoices) == 1:
                 invoice_to_show = invoices
             elif len(invoices) > 1:
                 action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
                 action['domain'] = [('id', 'in', invoices.ids)]
                 action['view_mode'] = 'tree,form'
                 return action
             else:
                 return {'type': 'ir.actions.act_window_close'} 
        else:
            invoice_to_show = self.invoice_id

        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        action['view_mode'] = 'form'
        action['res_id'] = invoice_to_show.id
        action['views'] = [(view_id, view_type) for view_id, view_type in action.get('views', []) if view_type == 'form']
        action.pop('domain', None)
        action['context'] = {'default_move_type': 'out_invoice'}
        return action