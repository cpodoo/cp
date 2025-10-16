# -*- coding: utf-8 -*-
from odoo import api, fields, models

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def send_birthday_notification(self):
        today = fields.Date.context_today(self)
        for employee in self.env['hr.employee'].search([('birthday', '!=', False), ('work_email', '!=', False)]):
            if employee.company_id.send_employee_birthday_notification and today == employee.birthday:
                template_id = self.env.ref('cp_birthday_notification.employee_birthday_notification_template')
                template_id.send_mail(employee.id, force_send=True)
