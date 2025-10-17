from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    image_128 = fields.Image(related='product_id.image_1920', string='Image')
    seq_no = fields.Integer(string='No.', compute="_compute_sequence")

    @api.depends('order_id.order_line')
    def _compute_sequence(self):
        for order in self.mapped('order_id'):
            sorted_lines = order.order_line.sorted(lambda line: line.sequence)
            for index, line in enumerate(sorted_lines):
                line.seq_no = index + 1