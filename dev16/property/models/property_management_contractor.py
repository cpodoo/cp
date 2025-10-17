from odoo import models, fields

class PropertyManagementContractor(models.Model):
    _name = "property.management.contractor"
    _description = "Contractors in Property Management"

    name = fields.Char(string="Contractor Name", default="Adnan")
    # property_ids = fields.One2many(
    #     "property.management",
    #     "property_contractor_id",
    #     string="property Ids",
    # )
    sequence = fields.Integer(string="Sequence")
