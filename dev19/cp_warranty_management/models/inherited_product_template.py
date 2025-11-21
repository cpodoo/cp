from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Warranty detail fields
    is_warranty = fields.Boolean("Is Warranty")
    period = fields.Integer("Warranty Period")
    duration = fields.Selection(
        [("days", "Days"), ("months", "Months"), ("years", "Years")], default="days"
    )
    is_allow_renew = fields.Boolean("Allow Renew?")
    renew_cost = fields.Float("Renew Cost")
    warranty_ids = fields.One2many("sr.product.warranty", "product_id")
