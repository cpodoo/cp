# -*- coding: utf-8 -*-

from odoo import models, fields


class Speciality(models.Model):
    _name = "speciality.data"
    _description = "Speciality Data"
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    name = fields.Char('Name',tracking=True)
    


























