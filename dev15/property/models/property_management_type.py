from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PropertyManagementType(models.Model):
    _name = "property.management.type"
    _description = "Property Management Type"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many(
        "property.management", "property_type_id", string="property Ids"
    )
    sequence=fields.Integer(string="Sequence")
