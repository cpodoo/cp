# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CrmLeadDeliverable(models.Model):
    _name = 'crm.lead.deliverable'
    _description = 'Opportunity Deliverable'

    lead_id = fields.Many2one('crm.lead', string='Opportunity')
    srno = fields.Integer(string='Sr No', compute='_compute_srno', store=True)
    year = fields.Char(string='Year')
    item = fields.Many2one('product.product', string='Deliverable Name', required=True)
    description = fields.Text(string='Description')
    quantity = fields.Float(string='Quantity')
    uom = fields.Many2one('uom.uom', string='Unit of Measure')
    display = fields.Boolean(string='Display', default=True)

    @api.depends('lead_id', 'lead_id.deliverable_ids')
    def _compute_srno(self):
        for record in self:
            if record.lead_id:
                mou_list = record.lead_id.deliverable_ids
                for index, mou in enumerate(mou_list, start=1):
                    mou.srno = index

    @api.onchange('item')
    def _onchange_item(self):
        for line in self:
            if line.item:
                line.description = line.item.display_name
                line.uom = line.item.uom_id.id
            else:
                line.description = False
                line.uom = False
