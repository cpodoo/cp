from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # product_size_id = fields.Many2many("inventory.product.size", string="Size")
    recipe_line_ids = fields.One2many(
        "product.recipe.line", "product_tmpl_id", string="Recipe Lines"
    )
    ingredient_ok = fields.Boolean('Ingredients')


class ProductRecipeLine(models.Model):
    _name = "product.recipe.line"
    _description = "Product Recipe Line"

    product_tmpl_id = fields.Many2one("product.template", string="Product Template")

    product_categ_id = fields.Many2one("product.category", string="Product Category")
    product_id = fields.Many2many("product.template", string="Product")
    default_product_id = fields.Many2one("product.template", string="Default Products")
    product_standard_qty = fields.Integer(string="Standard Qty")
    uom_id = fields.Many2one('uom.uom', string="Unit of Measure")
