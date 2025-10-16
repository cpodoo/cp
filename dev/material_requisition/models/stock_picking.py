from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    po_number = fields.Char(string="PO No")
    po_date = fields.Date(string="PO Date", dafault=fields.Date.today)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')


    @api.constrains('po_number', 'po_date', 'sale_id')
    def _check_po_matches_sale_order(self):
        for picking in self:
            # Only validate if PO fields are both filled
            if picking.sale_id and picking.po_number and picking.po_date:
                sale = picking.sale_id
                if picking.po_number != sale.po_number or picking.po_date != sale.po_date:
                    raise ValidationError("PO No and PO Date must match the related Sale Order.")
