# -*- coding: utf-8 -*-

from odoo import models, fields

class Drug(models.Model):
    _name = "drug"
    _description = "Drugs"

    name = fields.Char(string='Drug name',tracking=True)