# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime

class Prescription(models.Model):
    _name='prescription'
    _inherit = ['custom.invoice', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Prescription', required=True, copy=False, readonly=True,index=True, default=lambda self: _('New'))
    patient=fields.Many2one('res.partner','Patient',required=True)
    doctor=fields.Many2one('hr.employee','Physician',required=True)
    pharmacy=fields.Many2one('health.center.pharmacy','Pharmacy')
    date=fields.Date('Prescription Date',default=datetime.now())
    state=fields.Selection([('Draft','Draft'),('Invoiced','Invoiced'),('Cancel','Cancelled')],default='Draft',readonly=True)
    info=fields.Text()
    move_id = fields.Many2one('account.move', string='Invoice')
    invoice_count = fields.Integer(string='Invoice Count', compute='_compute_invoice_count')

    prescription_line=fields.One2many('prescription.line','prescription_id',required=True)

    def create_invoices(self):
        print("\n\n______________create_invoices()_________________")
        if not self.prescription_line:
            raise UserError(_("Please Create Prescription lines first."))

        invoice_obj = self.env['account.move']
        account_journal_obj = self.env['account.journal']
        inv_fields = invoice_obj.fields_get()
        # print("_________________inv_fields____________inv_fields___________",inv_fields)
        default_value = invoice_obj.default_get(inv_fields)
        print("__________________default_value___________default_value____",default_value)
        invoice_line = self.env['account.move.line']
        line_f = invoice_line.fields_get()
        default_line = invoice_line.default_get(line_f)
        print("__________________default_line___________default_get()______",default_line)

        journal_id = self.env['account.journal'].search([('type','=','sale'),('code','=','INV')], limit=1)
        if not journal_id:
            raise UserError(_("No sales journal with code 'INV' found."))

        default_value.update({
            'partner_id': self.patient.id,
            'invoice_date': self.date,
            'journal_id': journal_id.id,
            'move_type': 'out_invoice',  
            'invoice_line_ids': []
        })
        temp_invoice = invoice_obj.new(default_value)
        temp_invoice._onchange_partner_id()
        default_value['invoice_date_due'] = temp_invoice.invoice_date_due
        default_value['invoice_origin'] = self.name

        for line in self.prescription_line:
            default_value['invoice_line_ids'].append((0,0,line._prepare_invoice_line()))

        inv_id = invoice_obj.create(default_value)
        print("______________________updated_invoice_line______cc______",inv_id)

        self.move_id = inv_id.id
        self.write({'state': 'Invoiced'})
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
        action['res_id'] = inv_id.id
        if not inv_id:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def cancel(self):
        self.write({'state': 'Cancel'})
        return True

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('prescription') or '/'
        return super(Prescription, self).create(vals)

    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = self.env['account.move'].search_count([('invoice_origin', '=', rec.name)])

    def action_view_invoice(self):
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
            'default_move_type': 'out_invoice', 
        }
        if len(self) == 1:
            context.update({
                'default_partner_id': self.patient.id,
                'default_invoice_origin': self.mapped('name'),
                'default_user_id': self.doctor.id,
            })
        action['context'] = context
        return action

class PrescriptionLine(models.Model):
    _name='prescription.line'
    _description = "Prescription Line"

    @api.model
    def default_get(self, fields_list):
        res=super(PrescriptionLine,self).default_get(fields_list)
        if self._context.get('patient'):
            res.update({'patient': self._context.get('patient'),'pharmacy': self._context.get('pharmacy')})
        return res

    prescription_id=fields.Many2one('prescription')
    name=fields.Many2one('medicine','Medicine',required=True)
    indication=fields.Char()
    dose_form=fields.Char('Form')
    dose_route=fields.Char('Administration Route')
    start_treatment=fields.Date('Start of treatment')
    end_treatment=fields.Date('End of treatment')
    patient=fields.Many2one('res.partner')
    pharmacy=fields.Many2one('health.center.pharmacy')

    qty=fields.Integer('x')
    dose=fields.Integer('Dose')
    dose_unit=fields.Char()
    common_dosage=fields.Char()
    admin_times=fields.Char('Admin Hours')
    frequency=fields.Integer('Day(s)')
    frequency_unit=fields.Selection([('Seconds','Seconds'),('Minutes','Minutes'),('Hours','Hours'),
                                     ('Days','Days'),('Weeks','Weeks'),('Months','Months'),('When Required','When Required')],'Unit')

    duration=fields.Integer()
    duration_period=fields.Selection([('Minutes','Minutes'),('Hours','Hours'),
                                      ('Days','Days'),('Weeks','Weeks'),('Months','Months')],'Period')
    info=fields.Text()


    def _prepare_invoice_line(self):
        self.ensure_one()
        return {
            'name': self.name.name,
            'product_id': self.name.id,
            'quantity': self.dose,
            'price_unit': self.name.lst_price,
        }