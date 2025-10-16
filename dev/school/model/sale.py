from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_custom_note = fields.Char(string="Custom Note")

    def action_custom_button(self):
        for order in self:
            # Add your logic here
            order.message_post(body="Custom button clicked.")