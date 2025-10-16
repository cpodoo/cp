# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    opportunity_id = fields.Many2one('crm.lead', string='Opportunity')
