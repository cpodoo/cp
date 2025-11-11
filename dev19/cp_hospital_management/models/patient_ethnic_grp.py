# -*- coding: utf-8 -*-

# from os.path import join

from odoo import api, fields, models


class EthnicGroup(models.Model):
    _name = "ethnic.group"
    _description = "Ethnic Group"

    name = fields.Char('Name',tracking=True)
