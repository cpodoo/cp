# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime

class CustomInvoice(models.Model):
    _name="custom.invoice"
    _description = "Custom Invoice"

    invoice_count = fields.Integer(compute='_compute_invoice')

    def _compute_invoice(self):
        Invoice = self.env['account.move']
        self.invoice_count = Invoice.search_count([('invoice_origin', '=', self.name)])
        return True