# -*- coding: utf-8 -*-

from odoo import fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    po_product_line_ids = fields.One2many('purchase.product.history.line', 'product_history_id', string='Purchase History', compute='_compute_po_product_line_ids')

    def _compute_po_product_line_ids(self):
        self.po_product_line_ids = False
        order_line = self.env['purchase.order.line'].search([])
        product_po_order_line = order_line.filtered(lambda l: l.product_id and l.product_id.id == self.id)
        self.env['purchase.product.history.line'].create([{
            'product_history_id': self.id,
            'order_reference_id': line.order_id.id,
            'description': line.name,
            'price_unit': line.price_unit,
            'product_qty': line.product_qty,
            'price_subtotal': line.price_subtotal,
        } for line in product_po_order_line] if product_po_order_line else [])
