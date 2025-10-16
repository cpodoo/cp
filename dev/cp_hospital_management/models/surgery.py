# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Surgery(models.Model):
    _name = "surgery"
    _inherit = ['custom.invoice', 'mail.thread', 'mail.activity.mixin'] 
    _description = "Surgery Record"

    name = fields.Char(string='Surgery', required=True, copy=False, readonly=True,
                        states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    patient = fields.Many2one('res.partner', required=True)
    # computed_age = fields.Char(string='Age at time of Surgery', compute='_compute_computed_age', store=True)
    surgery_type_id = fields.Many2one('surgery.type', 'Surgery Type')
    surgery_end_date = fields.Datetime('Surgery End date & time')
    surgery_start_date = fields.Datetime('Surgery Start date & time')
    surgery_length = fields.Float('Duration', compute='_compute_surgery_length', store=True)

    classification = fields.Selection([('Optional', 'Optional'), ('Required', 'Required'), ('Urgent', 'Urgent'), ('Emergency', 'Emergency')], 'Urgency', required=True)
    surgeon = fields.Many2one('hr.employee', required=True)
    institution = fields.Many2one('health.center', 'Health Center', required=True)
    operating_room = fields.Many2one('health.center.ot', 'Operation Theater', required=True)
    building = fields.Many2one('health.center.building', required=True)
    anesthetist = fields.Many2one('hr.employee', required=True)
    signed_by = fields.Many2one('res.users', default=lambda self: self.env.user, required=True)
    state = fields.Selection([('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('In Progress', 'In Progress'), ('Done', 'Done'), ('Invoiced', 'Invoiced'),
                              ('Cancelled', 'Cancelled')], default='Draft')
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True, copy=False)

    surgery_date_time = fields.Datetime(tracking=True, string="Surgery Start Date & Time")
    # procedure_type = fields.Many2one('procedure', 'Procedure', required=True, copy=False, tracking=True)    
    doc_line_ids = fields.One2many('doc.surgery.line', 'surgery_id', string='Doctors', tracking=True, ondelete='cascade')
    nurse_line_ids = fields.One2many('nurse.surgery.line', 'surgery_id', string='Nurses', tracking=True, ondelete='cascade')

    # @api.depends('patient.birth_date', 'surgery_start_date')
    # def _compute_computed_age(self):
    #     for rec in self:
    #         if rec.patient.birth_date and rec.surgery_start_date:
    #             start_date = fields.Date.to_date(rec.surgery_start_date)
    #             birth_date = fields.Date.to_date(rec.patient.birth_date)
    #             age = relativedelta.relativedelta(start_date, birth_date).years
    #             rec.computed_age = str(age)
    #         else:
    #             rec.computed_age = False

    @api.depends('surgery_start_date', 'surgery_end_date')
    def _compute_surgery_length(self):
        for rec in self:
            if rec.surgery_start_date and rec.surgery_end_date:
                start = fields.Datetime.to_datetime(rec.surgery_start_date)
                end = fields.Datetime.to_datetime(rec.surgery_end_date)
                duration = (end - start).total_seconds() / 3600
                rec.surgery_length = duration
            else:
                rec.surgery_length = 0.0

    def action_surgery_confirm(self):
        self.write({'state': 'Confirmed'})

    def action_surgery_end(self):
        self.write({'state': 'Done', 'surgery_end_date': datetime.now()})

    def action_surgery_cancel(self):
        self.write({'state': 'Cancelled'})

    def action_surgery_set_to_draft(self):
        self.write({'state': 'Draft'})

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('surgery') or _('New')
        return super(Surgery, self).create(vals)

    def action_surgery_start(self):
        self.write({'state': 'In Progress', 'surgery_start_date': datetime.now()})

    def _prepare_invoice_line(self):
        self.ensure_one()
        vals = {
            'sequence': 10,
            'name': self.surgery_type_id.name,
            'quantity': 1.0,
            'discount': 0.0,
            'price_unit': self.surgery_type_id.charge,
        }
        return vals

    def create_invoices(self):
        invoice_obj = self.env['account.move']
        journal_id = self.env['account.journal'].search([('type', '=', 'sale'), ('code', '=', 'INV')], limit=1)
        if not journal_id:
            raise UserError(_('Please define a Sale journal with code INV.'))

        invoice_vals = {
            'partner_id': self.patient.id,
            'invoice_date': self.surgery_start_date.date() if self.surgery_start_date else fields.Date.today(),
            'journal_id': journal_id.id,
            'move_type': 'out_invoice',
            'invoice_origin': self.name,
            'invoice_line_ids': [(0, 0, self._prepare_invoice_line())],
        }
        invoice = invoice_obj.create(invoice_vals)
        self.invoice_id = invoice.id
        self.write({'state': 'Invoiced'})
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
        action['res_id'] = invoice.id
        return action

    def action_view_invoice(self):
        invoices = self.env['account.move'].search([('invoice_origin', '=', self.name)])
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
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
                'default_user_id': self.surgeon.id,
            })
        action['context'] = context
        return action


class SurgeryType(models.Model):
    _name = "surgery.type"
    _description = "Surgery Type"

    name = fields.Text('Surgery', required=True)
    charge = fields.Float('Surgery Charge')

    @api.model
    def create(self, vals):
        name = self.search([('name', '=', vals['name'])], limit=1)
        if name:
            raise UserError(_("Surgery Already Exist."))

        category_id = self.env['product.category'].search([('name', '=', 'Surgery')], limit=1).id
        if category_id:
            self.env['product.product'].create({
                'name': vals['name'],
                'type': 'service',
                'categ_id': category_id,
                'list_price': vals.get('charge', 0.0),
            })
        else:
            raise UserError(_("Product Category 'Surgery' not found."))
        return super(SurgeryType, self).create(vals)

    def write(self, vals):
        if vals:
            if vals.get('name'):
                name = self.search([('name', '=', vals['name'])], limit=1)
                if name and name != self:
                    raise UserError(_("Surgery Already Exist."))

            product = self.env['product.product'].search([('name', '=', self.name)], limit=1)
            if not product:
                raise UserError(_("This Surgery is no more exists in Products."))

            if vals.get('name'):
                product.name = vals['name']
            if vals.get('charge'):
                product.list_price = vals['charge']
        return super(SurgeryType, self).write(vals)

    def unlink(self):
        for rec in self:
            product = self.env['product.product'].search([('name', '=', rec.name)], limit=1)
            if product:
                product.unlink()
        return super(SurgeryType, self).unlink()


class DoctorSurgeryLine(models.Model):
    _name = "doc.surgery.line"
    _description = "Surgery Doctor Line"

    name = fields.Many2one('role.data', domain=[('type', '=', 'doc')], string='Role', tracking=True)
    doctor_id = fields.Many2one('res.partner', domain=[('is_doctor', '=', True)], string='Doctor', tracking=True)
    surgery_id = fields.Many2one('surgery', string='Surgery', tracking=True, ondelete='cascade')


class NurseSurgeryLine(models.Model):
    _name = "nurse.surgery.line"
    _description = "Surgery Nurse Line" 

    name = fields.Many2one('role.data', domain=[('type', '=', 'nurse')], string='Role', tracking=True)
    nurse_id = fields.Many2one('hr.employee', domain=[('is_nurse', '=', True)], string='Nurse', tracking=True)
    surgery_id = fields.Many2one('surgery', string='Surgery', tracking=True, ondelete='cascade')