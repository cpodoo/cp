from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')

    def create(self, vals):
        print("\n=== PURCHASE ORDER CREATE ===")
        print("Incoming vals:", vals)
        return super(PurchaseOrder, self).create(vals)

    def write(self, vals):
        print("\n=== PURCHASE ORDER WRITE ===")
        print("Updated vals:", vals)
        return super(PurchaseOrder, self).write(vals)

    def button_confirm(self):
        print("\n=== PURCHASE ORDER CONFIRM ===")
        return super(PurchaseOrder, self).button_confirm()


    def _prepare_picking(self):
        res = super()._prepare_picking()
        res['sale_order_id'] = self.sale_order_id.id
        return res