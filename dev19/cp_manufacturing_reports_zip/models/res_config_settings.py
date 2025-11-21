# -*- coding: utf-8 -*-

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mo_report_zip = fields.Many2one('ir.actions.report', related="company_id.mo_report_zip", readonly=False)


class ResCompany(models.Model):
    _inherit = 'res.company'

    mo_report_zip = fields.Many2one('ir.actions.report', default=lambda self: self.env.ref('mrp.action_report_production_order', raise_if_not_found=False))
