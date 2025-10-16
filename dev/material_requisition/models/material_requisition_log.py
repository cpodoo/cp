from odoo import models, fields, api


class MaterialRequisitionLog(models.Model):
    _name = 'material.requisition.log'
    _description = 'Material Requisition Log'

    delivery_expected = fields.Date(string='Delivery Expected')
    create_uid = fields.Many2one('res.users', string='Created By', readonly=True)

    line_ids = fields.One2many(
        'material.requisition.log.item',
        'requisition_id',
        string='Product Lines'
    )


class MaterialRequisitionLogItem(models.Model):
    _name = 'material.requisition.log.item'
    _description = 'Material Requisition Log Item'

    requisition_id = fields.Many2one(
        'material.requisition.log',
        string='Requisition Reference',
        ondelete='cascade',
        required=True
    )
    asset_name = fields.Many2one(
        'product.product',
        string='Asset/Material Name',
        required=True,
        domain=[('type', '=', 'product')]
    )
    description = fields.Text(string='Description')
    required_qty = fields.Float(string='Required Qty', required=True)
    available_qty = fields.Float(
        string='Available Qty',
        compute='_compute_available_qty',
        readonly=True
    )

    @api.depends('asset_name')
    def _compute_available_qty(self):
        for line in self:
            line.available_qty = line.asset_name.qty_available if line.asset_name else 0.0
