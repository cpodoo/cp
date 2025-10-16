from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "property.management.tag"
    _description = "Property Management Tag"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        (
            "unique_name",
            "UNIQUE(name)",
            "Tag name must be unique",
        ),
    ]
