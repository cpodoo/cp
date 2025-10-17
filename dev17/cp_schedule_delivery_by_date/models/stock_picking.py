# -*- coding: utf-8 -*-
from odoo import fields, models, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_datetime = fields.Datetime(string='Delivery Date')
