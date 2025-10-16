from odoo import models, fields

class Project(models.Model):
    _inherit = 'project.project'

    sale_order_id = fields.Many2one('sale.order', string="Sale Order")


# class ProjectTask(models.Model):
#     _inherit = 'project.task'
#
#     sale_order_id = fields.Many2one('sale.order', string='Sales Order')
