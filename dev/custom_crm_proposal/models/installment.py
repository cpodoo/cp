# -*- coding: utf-8 -*-
from odoo import models, fields


class ProposalInstallment(models.Model):
    _name = 'proposal.installment'
    _description = 'Proposal Installment'

    lead_id = fields.Many2one('crm.lead', string='Opportunity')
    year = fields.Char(string='Year')
    installment_no = fields.Integer(string='Installment No', required=True)
    date = fields.Date(string='Installment Date')
    percentage = fields.Float(string='Percentage (%)')
    amount = fields.Float(string='Installment Amount', required=True)
    display = fields.Boolean(string='Display', default=True)
    is_invoice = fields.Boolean(string="Is Invoiced", default=False)
    currency_id = fields.Many2one(
        related='lead_id.company_currency',
        depends=['lead_id.company_currency'],
        store=True,
        string='Currency'
    )
