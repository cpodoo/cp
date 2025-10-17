# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import date
from odoo.exceptions import ValidationError

class StockMove(models.Model):
    _inherit = 'stock.move'

    delivery_datetime = fields.Datetime(string='Delivery Date')

    def _get_new_picking_values(self):
        res = super(StockMove, self)._get_new_picking_values()
        if res.get('picking_type_id'):
            picking_type = self.env['stock.picking.type'].browse(res.get('picking_type_id'))
            if picking_type.code == 'outgoing':
                res['scheduled_date'] = self.delivery_datetime
        res['delivery_datetime'] = self.delivery_datetime
        return res

    def _search_picking(self, move):
        domain = [
            ('group_id', '=', move.group_id.id),
            ('location_id', '=', move.location_id.id),
            ('location_dest_id', '=', move.location_dest_id.id),
            ('picking_type_id', '=', move.picking_type_id.id),
            ('printed', '=', False),
            ('state', 'in', ['draft', 'confirmed', 'waiting', 'partially_available', 'assigned'])]
        if move.delivery_datetime:
            domain += [('delivery_datetime', '=', move.delivery_datetime)]
        return self.env['stock.picking'].search(domain, limit=1)

    @api.constrains('delivery_datetime')
    def _date_validation(self):
        for move in self:
            if move.delivery_datetime and move.delivery_datetime.date() < date.today():
                raise ValidationError("Date should be after the today date")

    def _assign_picking(self):
        for move in self:
            recompute = False
            picking = self._search_picking(move)
            if picking:
                if picking.partner_id.id != move.partner_id.id or picking.origin != move.origin:
                    picking.write({
                        'partner_id': False,
                        'origin': False,
                    })
            else:
                recompute = True
                picking = picking.create(move._get_new_picking_values())
            move.write({'picking_id': picking.id})
            move._assign_picking_post_process(new=recompute)
        return True
