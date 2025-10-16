from email.policy import default

from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    po_number = fields.Char(string="PO No.")
    po_date = fields.Date(string="PO Date", default=fields.Date.today)

    @api.model
    def create(self, vals):
        print("\n=== SALE ORDER CREATE ===")
        print("Incoming vals:", vals)

        # Assign PO No and Date if not provided
        if not vals.get('po_number'):
            vals['po_number'] = self.env['ir.sequence'].next_by_code('sale.order.po')

        return super(SaleOrder, self).create(vals)

    def write(self, vals):
        print("\n=== SALE ORDER WRITE ===")
        print("Updated vals:", vals)
        return super(SaleOrder, self).write(vals)

    def action_confirm(self):
        print("\n=== SALE ORDER CONFIRM ===")

        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for picking in order.picking_ids:
                picking.po_number = order.po_number
                picking.po_date = order.po_date
        return res
