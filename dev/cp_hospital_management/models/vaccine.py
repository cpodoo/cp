# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime

class Vaccine(models.Model):
    _name="vaccine"
    _inherit = ['mail.thread']
    _description = "Vaccine"

    name=fields.Many2one('medicine','Vaccine',required=True)
    patient=fields.Many2one('res.partner',required=True)
    dose=fields.Integer()
    date=fields.Datetime(default=datetime.now(),required=True)
    doctor=fields.Many2one('hr.employee',required=True)
    institution=fields.Many2one('health.center')
    info=fields.Text()