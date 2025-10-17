from odoo import api, fields, models

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    image_128 = fields.Image(related='product_id.image_1920', string='Image')
    seq_no = fields.Integer(string='No.',store=True, compute="_compute_sequence")

    @api.depends('order_id.order_line')
    def _compute_sequence(self):
        for order in self.mapped('order_id'):
            sorted_lines = order.order_line.sorted(lambda line: line.sequence)
            for index, line in enumerate(sorted_lines):
                line.seq_no = index + 1