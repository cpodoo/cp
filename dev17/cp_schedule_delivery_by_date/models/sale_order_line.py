# -*- coding: utf-8 -*-
from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    delivery_datetime = fields.Datetime(string='Delivery Date')

    def _prepare_procurement_values(self, group_id=False):
        res = super()._prepare_procurement_values(group_id)
        res['delivery_datetime'] = self.delivery_datetime
        if self.delivery_datetime:
            res['date_planned'] = self.delivery_datetime
        return res
