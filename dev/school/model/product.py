from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit = "product.category"

    is_ingredient_ok = fields.Boolean(' Is Ingredient')
