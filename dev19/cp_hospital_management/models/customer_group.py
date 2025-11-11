# -*- coding: utf-8 -*-

from odoo import models, fields

class CustomerGroup(models.Model):
    _name = "customer.group"
    _description = "Customer Group"
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    name = fields.Char(string='Group name',tracking=True)