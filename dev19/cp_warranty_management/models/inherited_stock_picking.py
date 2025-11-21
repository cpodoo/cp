from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        result = super(StockPicking, self).button_validate()

        # Create warranty records after delivery is validated
        if self.sale_id and self.state == 'done':
            self.sale_id.create_warranty_records(self.sale_id)

        # Iterate through product moves (Odoo 19)
        for move in self.move_ids:
            warranty = self.env["sr.product.warranty"].search([
                ("product_id", "=", move.product_id.product_tmpl_id.id),
                ("sale_order_id", "=", self.sale_id.id),
            ], limit=1)

            if warranty:
                # Iterate through stock move lines (Odoo 19)
                for move_line in move.move_line_ids:
                    if move_line.lot_id:
                        warranty.serial_number = move_line.lot_id.name

        return result

# from odoo import api, fields, models
#
# class StockPicking(models.Model):
#     _inherit = "stock.picking"
#
#     def button_validate(self):
#         result = super(StockPicking, self).button_validate()
#         if self.sale_id and self.state == 'done':
#             self.sale_id.create_warranty_records(self.sale_id)
#         if self.move_ids_without_package:
#             for line in self.move_ids_without_package:
#                 warranty_id = self.env["sr.product.warranty"].search(
#                     [
#                         ("product_id", "=", line.product_tmpl_id.id),
#                         ("sale_order_id", "=", self.origin),
#                     ]
#                 )
#                 if warranty_id:
#                     for lot in line.lot_ids:
#                         warranty_id.serial_number = lot.name
#         return result
