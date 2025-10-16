from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    print_tax = fields.Boolean(string="Print Tax", default=True)
    print_final_price = fields.Boolean(string="Sell Price", default=False)

    def action_print_retail_bill(self):
        return self.env.ref('tax_print.action_report_saleorder_retail_bill').report_action(self)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    print_final_price = fields.Boolean(related='order_id.print_final_price', string="Show Final Price", readonly=False)
    final_price = fields.Monetary(
        string="Final Price",
        compute='_compute_final_price',
        store=True,
        currency_field='currency_id'
    )

    @api.depends('price_unit', 'product_id.standard_price')
    def _compute_final_price(self):
        for line in self:
            line.final_price = line.price_unit - line.product_id.standard_price
