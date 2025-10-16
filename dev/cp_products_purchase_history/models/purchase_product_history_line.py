# -*- coding: utf-8 -*-

from odoo import fields, models

class PurchaseProductHistoryLine(models.Model):
    _name = 'purchase.product.history.line'
    _description = 'Product history line for product'

    product_history_id = fields.Many2one('product.product', string='Product')
    order_reference_id = fields.Many2one('purchase.order', string='Order')
    description = fields.Text(string='Description')
    price_unit = fields.Float(string='Unit Price')
    product_qty = fields.Float(string='Quantity')
    price_subtotal = fields.Float(string='Subtotal')
