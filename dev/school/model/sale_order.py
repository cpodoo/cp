from odoo import api, models, fields
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'  # Inherit the sale.order model

    discount_code = fields.Char(string='Discount Code')


    def action_confirm(self):
        # Add custom logic before confirming the sale order
        for order in self:
            if not order.discount_code:
                raise UserError("Please provide a discount code before confirming.")
        # Call the original action_confirm method
        return super(SaleOrder, self).action_confirm()


    def apply_discount_code(self):
        for order in self:
            if order.discount_code:
                # Add logic to apply the discount code
                order.amount_total *= 0.9  # Example: 10% discount
            else:
                raise UserError("No discount code provided.")