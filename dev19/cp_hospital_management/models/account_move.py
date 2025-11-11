# -*- coding: utf-8 -*-

from datetime import date
from odoo.exceptions import UserError
from odoo import api, fields, models, _

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.model
    def _default_account(self):
    	print("__________________default_account______________________",self,self._context)
    	if self._context.get('journal_id'):
    		journal = self.env['account.journal'].browse(self._context.get('journal_id'))
    		print("______________journal_______________________",journal)
    		if self._context.get('type') in ('out_invoice', 'in_refund'):
    			print("_____________________journal.default_credit_account_id.id_____________",journal.default_credit_account_id,journal.default_credit_account_id.id)
    			return journal.default_credit_account_id.id
    		print("++++++++++journal.default_credit_account_id.id+++++++++++",journal.default_credit_account_id,journal.default_credit_account_id.id)
    		return journal.default_debit_account_id.id