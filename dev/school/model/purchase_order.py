from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    x_purchase_reference = fields.Char(string="Custom Reference")
    x_priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string="Priority")

    x_delivery_date = fields.Date(string="Expected Delivery Date")

    x_internal_note = fields.Text(string="Internal Note")
    def action_custom_purchase_button(self):
        for order in self:
            order.message_post(body="Custom Purchase button clicked.")