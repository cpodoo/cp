from odoo import models, fields

class ProjectProject(models.Model):
    _inherit = 'project.project'

    x_client_name = fields.Char(string="Client Name")
