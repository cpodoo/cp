from odoo import fields,api,models

class BrandBrand(models.Model):
    _name = 'brand.brand'
    _description = "Brand"

    name=fields.Char(string="Name",required=True)
    description=fields.Text(string="Description")

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The brand name must be unique. Please choose a different name.')
    ]