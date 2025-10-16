# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons.base.models.res_currency import Currency


class CrmSaleOrderLine(models.Model):
    _name = 'crm.sale.order.line'
    _description = 'CRM Sales Order Line'

    lead_id = fields.Many2one('crm.lead', string="Opportunity", required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", domain="[('sale_ok', '=', True)]", change_default=True)
    name = fields.Text(string="Description", required=True)
    product_uom_qty = fields.Float(string="Quantity", default=1.0, digits='Product Unit of Measure', required=True)
    price_unit = fields.Float(string="Unit Price", digits='Product Price', required=True)
    tax_ids = fields.Many2many('account.tax', string="Taxes", domain=[('type_tax_use', '=', 'sale')])

    currency_id = fields.Many2one(
        related='lead_id.company_currency',
        depends=['lead_id.company_currency'],
        store=True,
        string='Currency'
    )
    price_subtotal = fields.Monetary(
        string="Subtotal",
        compute="_compute_amount",
        store=True,
        currency_field='currency_id'
    )
    price_total = fields.Monetary(
        string="Total",
        compute="_compute_amount",
        store=True,
        currency_field='currency_id'
    )
    display = fields.Boolean(string='Display', default=True)

    @api.onchange('product_id')
    def _onchange_product(self):
        for line in self:
            if line.product_id:
                line.name = line.product_id.display_name
            else:
                line.name = False

    @api.depends('product_uom_qty', 'price_unit', 'tax_ids', 'lead_id.partner_id')
    def _compute_amount(self):
        for line in self:
            currency = line.currency_id or line.lead_id.company_id.currency_id or self.env.company.currency_id
            price = line.price_unit
            taxes = line.tax_ids.compute_all(
                price,
                currency=currency,
                quantity=line.product_uom_qty,
                product=line.product_id,
                partner=line.lead_id.partner_id
            )
            line.update({
                'price_subtotal': taxes['total_excluded'],
                'price_total': taxes['total_included'],
            })
