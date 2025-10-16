from odoo import models, fields

class ProjectProject(models.Model):
    _inherit = 'project.project'

    x_project_type = fields.Selection([
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('infrastructure', 'Infrastructure'),
    ], string='Project Type')
