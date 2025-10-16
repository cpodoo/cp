# -*- coding: utf-8 -*-

from odoo import models, fields


class Allergy(models.Model):
    _name = "allergy"
    _description = "Patient Allergy"

    name = fields.Char(string='Allergy', tracking=True)