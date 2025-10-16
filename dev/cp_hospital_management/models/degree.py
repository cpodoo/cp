# -*- coding: utf-8 -*-

from odoo import models, fields

class Degree(models.Model):
    _name = "degree.data"
    _description = "Degree Data"
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    name = fields.Char('Name',tracking=True)
    doc_id = fields.Many2one('res.partner',string='Doctor',tracking=True)