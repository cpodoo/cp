# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime

class InPatientAdmissions(models.Model):
    _name = 'inpatient.admissions'
    _description = "Inpatient Admissions"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Inpatient', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    patient=fields.Many2one('res.partner','Patient',required=True)
    addmission_type=fields.Selection([('urgent','Urgent'),('maternity','Maternity')],string="Addmission Type")
    institution = fields.Many2one('health.center', 'Health Center', required=True)
    building = fields.Many2one('health.center.building', required=True)
    ward=fields.Many2one('health.center.ward',string="Ward")
    bed=fields.Many2one('health.center.beds')
    hospitallization_date=fields.Datetime(default=datetime.now(),required=True)
    discharge_date=fields.Datetime()

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('inpatient.admissions') or 'New'
        return super(InPatientAdmissions, self).create(vals)