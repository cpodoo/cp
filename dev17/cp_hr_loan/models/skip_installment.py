# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta

class cp_skip_installment(models.Model):
    _name = 'cp.skip.installment'
    _description = 'cp Skip Installment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    reject_reason = fields.Text(string="Reject Reason", copy=False, tracking=True)

    def action_open_skip_reject_wizard(self):
        self.ensure_one()

        rejection_source = None
        if self.state == 'request':
            rejection_source = 'manager'
        elif self.state == 'approve':
            rejection_source = 'hr'
        else:
            raise UserError("Cannot reject skip request from state '%s'." % self.state)

        wizard_context = {
            'default_skip_installment_id': self.id,
            'default_reason': '',
            'rejection_source': rejection_source
        }

        return {
            'type': 'ir.actions.act_window',
            'name': 'Provide Skip Rejection Reason', 
            'res_model': 'skip.installment.reject.reason',
            'view_mode': 'form',
            'view_id': self.env.ref('cp_hr_loan.skip_installment_reject_reason_wizard_view_form').id,
            'target': 'new',
            'context': wizard_context
        }

    @api.model
    def _get_employee(self):
        employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
        return employee_id

    @api.model
    def _get_default_user(self):
        return self.env.user

    name = fields.Char('Name', default='/')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, default=_get_employee)
    loan_id = fields.Many2one('employee.loan', string='Loan', required=True)
    installment_id = fields.Many2one('installment.line', string='Installment', required=True)
    date = fields.Date('Date', default=fields.date.today())
    user_id = fields.Many2one('res.users', string='User', default=_get_default_user)
    notes = fields.Text('Reason', required=True)
    manager_id = fields.Many2one('hr.employee', string='Department Manager', required=True)
    skip_installment_url = fields.Char('URL', compute='get_url')
    hr_manager_id = fields.Many2one('hr.employee', string='HR Manager')
    state = fields.Selection([('draft', 'Draft'),
                              ('request', 'Submit Request'),
                              ('approve', 'Approve'),
                              ('confirm', 'Confirm'),
                              ('done', 'Done'),
                              ('reject', 'Reject'),
                              ('cancel', 'Cancel'), ], string='State', default='draft', tracking=True)

    def get_url(self):
        for installment in self:
            ir_param = self.env['ir.config_parameter'].sudo()
            base_url = ir_param.get_param('web.base.url')
            action_id = self.env.ref('cp_hr_loan.action_cp_skip_installment').id
            menu_id = self.env.ref('cp_hr_loan.menu_skip_installment').id
            if base_url:
                base_url += '/web#id=%s&action=%s&model=%s&view_type=form&cids=&menu_id=%s' % (
                installment.id, action_id, 'cp.skip.installment', menu_id)
            installment.skip_installment_url = base_url

    @api.constrains('installment_id')
    def _Check_skip_installment(self):
        request_ids = False
        if self.employee_id and self.installment_id:
            request_id = self.search([('employee_id', '=', self.employee_id.id),
                                      ('installment_id', '=', self.installment_id.id),
                                      ('state', 'in', ['draft', 'approve', 'confirm', 'done']), ('id', '!=', self.id)])
        request = len(request_id)
        if request > 0:
            raise ValidationError("This %s  installment of skip request has been %s state" % (
            self.installment_id.name, request_id.state))

    @api.onchange('loan_id')
    def onchange_loan_id(self):
        if self.loan_id:
            self.manager_id = self.loan_id.manager_id

    def action_send_request(self):
        if not self.manager_id:
            raise ValidationError(_('Please Select Department manager'))
        if self.manager_id and self.manager_id.id != self.loan_id.manager_id.id:
            raise ValidationError(_('Loan Manager and selected department manager not same'))
        if self.manager_id and self.manager_id.work_email:
            ir_model_data = self.env['ir.model.data']
            template_id = ir_model_data._xmlid_lookup('cp_hr_loan.skip_cp_manager_approval')[1]

            mtp = self.env['mail.template']
            template_id = mtp.browse(template_id)
            template_id.write({'email_to': self.manager_id.work_email})
            s = template_id.send_mail(self.ids[0], True)
        self.state = 'request'

    def get_hr_manager_email(self):
        group_id = self.env['ir.model.data']._xmlid_lookup('hr.group_hr_manager')[1]
        group_ids = self.env['res.groups'].browse(group_id)
        email = ''
        if group_ids:
            employee_ids = self.env['hr.employee'].search([('user_id', 'in', group_ids.users.ids)])
            for emp in employee_ids:
                if email:
                    email = email + ',' + emp.work_email
                else:
                    email = emp.work_email
        return email

    def approve_skip_installment(self):
        email = self.get_hr_manager_email()
        if email:
            ir_model_data = self.env['ir.model.data']
            template_id = ir_model_data._xmlid_lookup('cp_hr_loan.skip_ins_hr_manager_request')[1]

            mtp = self.env['mail.template']
            template_id = mtp.browse(template_id)
            template_id.write({'email_to': email})
            template_id.send_mail(self.ids[0], True)
        self.state = 'approve'

    # def cp_reject_skip_installment(self):
    #     if self.employee_id.work_email:
    #         ir_model_data = self.env['ir.model.data']
    #         template_id = ir_model_data._xmlid_lookup('cp_hr_loan.cp_manager_reject_skip_installment')[1]

    #         mtp = self.env['mail.template']
    #         template_id = mtp.browse(template_id)
    #         template_id.write({'email_to': self.employee_id.work_email})
    #         template_id.send_mail(self.ids[0], True)

    #     self.state = 'reject'

    # def hr_reject_skip_installment(self):
    #     employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
    #     self.hr_manager_id = employee_id and employee_id.id or False
    #     if self.employee_id.work_email and self.hr_manager_id:
    #         ir_model_data = self.env['ir.model.data']
    #         template_id = ir_model_data._xmlid_lookup('cp_hr_loan.hr_manager_reject_skip_installment')[1]

    #         mtp = self.env['mail.template']
    #         template_id = mtp.browse(template_id)
    #         template_id.write({'email_to': self.employee_id.work_email})
    #         template_id.send_mail(self.ids[0], True)

    #     self.state = 'reject'

    def confirm_skip_installment(self):
        employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
        self.hr_manager_id = employee_id and employee_id.id or False
        if self.employee_id.work_email and self.hr_manager_id:
            ir_model_data = self.env['ir.model.data']
            template_id = ir_model_data._xmlid_lookup('cp_hr_loan.hr_manager_confirm_skip_installment')[1]

            mtp = self.env['mail.template']
            template_id = mtp.browse(template_id)
            template_id.write({'email_to': self.employee_id.work_email})
            template_id.send_mail(self.ids[0], True)

        self.state = 'confirm'

    def skip_installment_done(self):
        date = self.installment_id.date
        date = date
        date = date + relativedelta(months=1)
        vals = {
            'name': str(self.installment_id.name) + ' - COPY',
            'employee_id': self.employee_id and self.employee_id.id or False,
            'date': date,
            'amount': self.installment_id.amount,
            'interest': 0.0,
            'installment_amt': self.installment_id.installment_amt,
            'ins_interest': 0.0,
            'loan_id': self.installment_id.loan_id.id,
        }
        new_inst = self.env['installment.line'].create(vals)
        if new_inst:
            self.installment_id.is_skip = True
        self.state = 'done'

    def skip_installment_cancel(self):
        self.state = 'cancel'

    def set_to_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'cp.skip.installment') or '/'
        return super(cp_skip_installment, self).create(vals)

    def copy(self, default=None):
        if default is None:
            default = {}
        default['name'] = '/'
        return super(cp_skip_installment, self).copy(default=default)

    def unlink(self):
        for skp_installment in self:
            if skp_installment.state != 'draft':
                raise ValidationError(_('Skip Installment delete in draft state only !!!'))
        return super(cp_skip_installment, self).unlink()