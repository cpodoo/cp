# -*- coding: utf-8 -*-

from odoo import fields, models

class PurchaseTemplateHistoryLine(models.Model):
    _name = 'purchase.template.history.line'
    _description = 'Purchase history line for template'

    history_id = fields.Many2one('product.template', string='Product')
    order_reference_id = fields.Many2one('purchase.order', string='Order')
    description = fields.Text(string='Description')
    price_unit = fields.Float(string='Unit Price')
    product_qty = fields.Float(string='Quantity')
    price_subtotal = fields.Float(string='Subtotal')
