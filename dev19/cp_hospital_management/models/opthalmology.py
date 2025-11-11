# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class Opthalmology(models.Model):
    _name='opthalmology'
    _description = "Opthalmology"

    patient=fields.Many2one('res.partner')
    doctor=fields.Many2one('hr.employee')
    visit_date=fields.Datetime('Date')