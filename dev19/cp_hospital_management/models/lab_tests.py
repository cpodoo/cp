# -*- coding: utf-8 -*-

from datetime import date
from odoo.exceptions import UserError
from odoo import api, fields, models, _

class LabTests(models.Model):
    _name = 'lab.tests'
    _inherit = ['custom.invoice', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Lab Test', required=True, copy=False, readonly=True,index=True, default=lambda self: _('New'))
    patient=fields.Many2one('res.partner','Patient',required=True)
    date_requested=fields.Date(default=date.today())
    physician_id=fields.Many2one('hr.employee','Physician')
    pathologist_id=fields.Many2one('hr.employee','Pathologist')
    date_analysis=fields.Date("Date of the anlysis")
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True, copy=False)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'Test in Progress'),
        ('completed', 'Completed'),
        ('invoiced', 'Invoiced'),
    ],string='Test Status', readonly=True, default='draft')
    test_line = fields.One2many('lab.tests.line', 'test_id', string='Test Lines', copy=True)

    def create_invoices(self):

        if not self.test_line:
            raise UserError(_("Please select atleast one test in test line."))

        invoice_obj = self.env['account.move']
        inv_fields = invoice_obj.fields_get()
        default_value = {}
        invoice_line = self.env['account.move.line']
        line_f = invoice_line.fields_get()
        default_line = invoice_line.default_get(line_f)
        print("_____________default_line_____________1111______________",default_line)

        journal_id = self.env['account.journal'].search([('type','=','sale'),('code','=','INV')])

        default_value.update({'partner_id': self.patient.id, 'invoice_date': self.date_requested, 'journal_id': journal_id.id})
        invoice = invoice_obj.new(default_value)
        invoice._onchange_partner_id()
        print("____________invoice__________default_value___________",invoice,default_value)
        default_value.update({'invoice_date_due': invoice.invoice_date_due, 'invoice_origin': self.name,'move_type':'out_invoice','invoice_line_ids': []})
        
        print("___________________journal_id____________________",journal_id)
        for line in self.test_line:
            default_value['invoice_line_ids'].append((0,0,line._prepare_invoice_line()))
        inv_id = invoice.create(default_value)
        self.invoice_id = inv_id.id
        self.write({'state': 'invoiced'})
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
        action['res_id'] = inv_id.id
        if not inv_id:
            action = {'type': 'ir.actions.act_window_close'}
        return action


    def start_test(self):
        self.write({'state': 'progress'})
        return True

    def complete_test(self):
        self.write({'state': 'completed'})
        return True

    def cancel(self):
        self.write({'state': 'cancel'})
        return True

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('lab.tests') or '/'
        return super(LabTests, self).create(vals)


    def action_view_invoice(self):
        print("_________________action_view_invoice______________13______",self)
        account_move_id = self.env['account.move'].search([('invoice_origin','=',self.name)])
        print("_________________action_view_invoice______________13______",account_move_id)
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        if len(account_move_id) > 1:
            action['domain'] = [('id', 'in', account_move_id.ids)]
        elif len(account_move_id) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = account_move_id.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

class LabTestsLine(models.Model):
    _name='lab.tests.line'
    _order="sequence"
    _description = "Lab Tests Line"

    test_id = fields.Many2one('lab.tests', string='Test Reference')
    sequence = fields.Integer(default=10)
    test_type = fields.Many2one('lab.tests.type')
    result=fields.Float()
    range=fields.Char("Normal Range",compute="_compute_range_units", store=True)
    units=fields.Char(compute="_compute_range_units", store=True)

    @api.depends('test_type')
    def _compute_range_units(self):
        for line in self:
            range = self.env['lab.tests.type'].search([('name', '=', line.test_type.name)]).range
            line.range = range
            units = self.env['lab.tests.type'].search([('name', '=', line.test_type.name)]).units
            line.units = units


    def _prepare_invoice_line(self):
        self.ensure_one()
        vals = {
            'sequence': self.sequence,
            'name': self.test_type.name,
            'product_id': self.test_type.product_id.id or False,
            'quantity': 1,
            'price_unit': self.test_type.product_id.list_price or 0.0,
        }
        return vals

class LabTestsType(models.Model):
    _name = 'lab.tests.type'
    _description = "Lab Tests Type"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    range = fields.Char("Normal Range", required=True)
    units = fields.Char("units", required=True)
    product_id = fields.Many2one('product.product', help='automated created related product_id when there is new lab test type') #
    price = fields.Float()

    @api.model
    def create(self, vals):

        name = self.search([('name', '=', vals['name'])])
        if name:
            raise UserError(_("Lab Test Already Exist."))

        category_id = self.env['product.category'].search([('name', '=', 'Lab Test')]).id

        product_id = self.env['product.product'].create({
            'name': vals['name'],
            'type': 'service',
            'categ_id': category_id,
            'list_price': vals.get('lst_price', 0.0),
        })
        res = super(LabTestsType, self).create(vals)
        for record in res:
            record.product_id = product_id
        return res

    def write(self, vals):
        if vals:
            if vals.get('name'):
                name = self.search([('name', '=', vals['name'])])
                if name:
                    raise UserError(_("Lab Test Already Exist."))

            product = self.env['product.product'].search([('name', '=', self.name)])
            if not product:
                raise UserError(_("This Lab Test is no more exist in product."))
            if vals.get('name'):
                product.name = vals['name']
            if vals.get('price'):
                product.list_price = vals['price']

        return super(LabTestsType, self).write(vals)

    def unlink(self):
        self.env['product.product'].search([('name', '=', self.name)]).unlink()
        return super(LabTestsType, self).unlink()

class ProductCategory(models.Model):
    _inherit = 'product.category'

    def unlink(self):
        category_lab_test = self.env.ref('globalteckz_hospital_management.category_lab_test', False)
        if category_lab_test:
            self = self - category_lab_test

        return super(ProductCategory, self).unlink()