from odoo import models, fields, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_notes = fields.Text(string='Custom Notes')
    delivery_instructions = fields.Text(string='Delivery Instructions')
    delivery_time = fields.Float(string='Estimated Delivery Time (hrs)')

    project_count = fields.Integer(string='Project Count', compute='_compute_project_count')

    def _compute_project_count(self):
        for order in self:
            order.project_count = self.env['project.project'].search_count([
                ('sale_order_id', '=', order.id)
            ])

    def action_view_projects(self):
        self.ensure_one()

        try:
            list_view = self.env.ref('project.project_project_tree_view').id
            form_view = self.env.ref('project.edit_project').id
        except ValueError:
            raise UserError(_("Project views not found. Please make sure the Project module is fully installed."))

        return {
            'name': _('Projects'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'view_mode': 'list,form',
            'views': [(list_view, 'list'), (form_view, 'form')],
            'domain': [('sale_order_id', '=', self.id)],
            'context': {'default_sale_order_id': self.id},
        }
