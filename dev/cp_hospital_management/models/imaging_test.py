# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ImagingTest(models.Model):
    _name="imaging.test"
    _inherit = ['custom.invoice', 'mail.thread', 'mail.activity.mixin'] 

    name = fields.Char(string='Test', required=True, copy=False, readonly=True,index=True, default=lambda self: _('New'))
    patient=fields.Many2one('res.partner',required=True)
    requestor=fields.Many2one('hr.employee','Doctor who requested the test')
    date_requested=fields.Datetime()
    date_analysis=fields.Datetime()
    image1=fields.Binary()
    image2=fields.Binary()
    image3=fields.Binary()
    image4=fields.Binary()
    image5=fields.Binary()
    image6=fields.Binary()
    analysis=fields.Text()
    conclusion=fields.Text()
    state=fields.Selection([('Draft','Draft'),('Test In Progress','Test In Progress'),('Completed','Completed'),('Invoiced','Invoiced')],default="Draft")
    test_type=fields.Many2one('imaging.test.type',required=True)
    invoice_id = fields.Many2one('account.move', string="Invoice")

    def test_start(self):
        self.write({'state':'Test In Progress'})

    def test_complete(self):
        self.write({'state':'Completed'})

    def cancel(self):
        self.write({'state': 'Cancelled'})
        return True


    def _prepare_invoice_line(self):
        self.ensure_one()

        product = self.env['product.product'].search([('name', '=', self.test_type.name)], limit=1)
        if not product:
            raise UserError(_('Product not found for imaging test type "%s"') % self.test_type.name)

        account = product.property_account_income_id or product.categ_id.property_account_income_categ_id
        if not account:
            raise UserError(_('No income account defined for product: %s') % product.name)

        return {
            'product_id': product.id,
            'name': product.name,
            'quantity': 1,
            'price_unit': product.list_price,
            'account_id': account.id,
            # 'display_type': False,  # important: real line
        }


    def create_invoices(self):
        invoice_obj = self.env['account.move']
        inv_fields = invoice_obj.fields_get()
        default_value = invoice_obj.default_get(inv_fields)

        invoice_line = self.env['account.move.line']
        line_f = invoice_line.fields_get()
        default_line = invoice_line.default_get(line_f)

        journal_id = self.env['account.journal'].search([('type','=','sale'),('code','=','INV')])

        default_value.update({'partner_id': self.patient.id, 'invoice_date': self.date_analysis, 'journal_id': journal_id.id})
        invoice = invoice_obj.new(default_value)
        invoice._onchange_partner_id()
        default_value.update({'invoice_date_due': invoice.invoice_date_due, 'invoice_origin': self.name,'move_type':'out_invoice','invoice_line_ids': []})

        default_value['invoice_line_ids'].append((0,0,self._prepare_invoice_line()))

        inv_id = invoice.create(default_value)
        self.invoice_id = inv_id.id
        self.write({'state': 'Invoiced'})
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
        action['res_id'] = inv_id.id
        if not inv_id:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('imaging.test') or '0'
        return super(ImagingTest, self).create(vals)

    def action_view_invoice(self):
        # invoices = self.mapped('invoice_ids')
        invoices = self.env['account.move'].search([('invoice_origin','=',self.name)])
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_type': 'out_invoice',
        }
        if len(self) == 1:
            context.update({
                'default_patient_id': self.patient.id,
                'default_invoice_origin': self.mapped('name'),
                'default_requestor_id': self.requestor.id,
            })
        action['context'] = context
        return action        
        
    
class ImagingTestType(models.Model):
    _name = "imaging.test.type"
    _description = "Imaging Test Type"

    code=fields.Char(required=True)
    test_charge=fields.Float(required=True)
    name=fields.Char(required=True,size=128)

    @api.model
    def create(self, vals):
        if 'name' in vals:
            name = self.search([('name', '=', vals['name'])])
            if name:
                raise UserError(_("Test Already Exist."))

        if 'code' in vals:
            code = self.search([('code', '=', vals['code'])])
            if code:
                raise UserError(_("Code Already Exist."))

        if 'name' in vals and 'test_charge' in vals:
            category_id = self.env['product.category'].search([('name', '=', 'Imaging Test')], limit=1).id

            self.env['product.product'].create({
                'name': vals['name'],
                'type': 'consu',
                'categ_id': category_id,
                'list_price': vals['test_charge'],
            })

        return super(ImagingTestType, self).create(vals)

    def write(self, vals):
        if vals:
            if vals.get('name'):
                name = self.search([('name', '=', vals['name'])])
                if name:
                    raise UserError(_("Test Already Exist."))
            if vals.get('code'):
                code = self.search([('code', '=', vals['code'])])
                if code:
                    raise UserError(_("Code Already Exist."))

            product = self.env['product.product'].search([('name', '=', self.name)])
            if not product:
                raise UserError(_("Your Previous Imaging test name doesn't match to any Product."))

            if vals.get('name'):
                product.name = vals['name']
            if vals.get('test_charge'):
                product.list_price = vals['test_charge']

        return super(ImagingTestType, self).write(vals)

    def unlink(self):
        self.env['product.product'].search([('name', '=', self.name)]).unlink()
        return super(ImagingTestType, self).unlink()