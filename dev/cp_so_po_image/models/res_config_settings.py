from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_product_image_report = fields.Boolean(
        string="Show Product Image",
        config_parameter='cp_so_po_image.sale_product_image_report',
        help='Show product Image in sale report')

    purchase_product_image_report = fields.Boolean(
        string="Show Product Image",
        config_parameter='cp_so_po_image.purchase_product_image_report',
        help='Show product Image in purchase report')