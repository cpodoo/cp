# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime

class CallLog(models.Model):
    _name="call.log"
    _description = "Call Log"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name=fields.Char('Call Log',readonly=True)
    patient=fields.Many2one('res.partner',required=True)
    person_in_charge=fields.Many2one('res.users',default=lambda self: self.env.user)
    call_type=fields.Selection([('Phone','Phone'),('Email','Email'),('SMS','SMS'),('Other','Other')],required=True)
    log_date=fields.Datetime('Date/Time of conrtact',default=datetime.now(),required=True)
    call_log=fields.Text()

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('call.log') or '0'
        return super(CallLog, self).create(vals)   