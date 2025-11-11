# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError


class AllowedSurgeon(models.Model):
    _name = "allowed.surgeon"
    _description = "Allowed Surgeon for Partner"

    surgeon_id = fields.Many2one('res.partner',domain=[('role','=ilike','Surgeon')],string='Surgeon', tracking=True)
    partner_id = fields.Many2one('res.partner',string='Partner', tracking=True)

  
 