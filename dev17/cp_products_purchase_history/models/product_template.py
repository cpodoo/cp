# -*- coding: utf-8 -*-

from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    po_history_line_ids = fields.One2many('purchase.template.history.line', 'history_id', string='Purchase history', compute='_compute_po_history_line_ids')

    def _compute_po_history_line_ids(self):
        self.po_history_line_ids = False
        order_line = self.env['purchase.order.line'].search([('product_id', 'in', self.product_variant_ids.ids)])
        self.env['purchase.template.history.line'].create([{
            'history_id': self.id,
            'order_reference_id': rec.order_id.id,
            'description': rec.name,
            'price_unit': rec.price_unit,
            'product_qty': rec.product_qty,
            'price_subtotal': rec.price_subtotal
        } for rec in order_line])
