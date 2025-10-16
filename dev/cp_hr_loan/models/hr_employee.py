# -*- coding: utf-8 -*-

from odoo import models, fields, api


class hr_employee(models.Model):
    _inherit = 'hr.employee'

    loan_request = fields.Integer('Loan Request Per Year', default=1, required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')

    @api.model
    def create(self, vals):
        employee = super(hr_employee, self).create(vals)

        partner = self.env['res.partner'].search([
            '|',
            ('email', '=', vals.get('work_email')),
            ('phone', '=', vals.get('work_phone'))
        ], limit=1)

        if not partner:
            partner_vals = {
                'name': vals.get('name'),
                'email': vals.get('work_email'),
                'phone': vals.get('work_phone'),
            }
            partner = self.env['res.partner'].create(partner_vals)

        employee.partner_id = partner.id

        return employee

    def action_update_partner(self):
        for emp in self:
            partner = self.env['res.partner'].search([('name', '=', emp.name)], limit=1)
            if partner:
                emp.partner_id = partner.id
            else:
                partner = self.env['res.partner'].create({
                    'name': emp.name,
                    'email': emp.work_email or '',
                    'phone': emp.work_phone or '',
                })
                emp.partner_id = partner.id



class hr_employee_public(models.Model):
    _inherit = 'hr.employee.public'

    loan_request = fields.Integer('Loan Request Per Year', default=1, required=True)


