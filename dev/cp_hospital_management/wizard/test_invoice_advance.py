# -*- coding: utf-8 -*-


import time


from odoo import api, fields, models, _
from odoo.exceptions import UserError

class TestsAdvancePaymentInv(models.TransientModel):
    _name = "tests.advance.payment.inv"
    _description = "Tests Advance Payment Invoice"

    @api.model
    def _count(self):
        return len(self._context.get('active_ids', []))

    @api.model
    def _get_advance_payment_method(self):
        if self._count() == 1:
            sale_obj = self.env['sale.order']
            order = sale_obj.browse(self._context.get('active_ids'))[0]
            if all([line.product_id.invoice_policy == 'order' for line in order.order_line]) or order.invoice_count:
                return 'all'
        return 'delivered'

    @api.model
    def _default_product_id(self):
        product_id = self.env['ir.values'].get_default('sale.config.settings', 'deposit_product_id_setting')
        return self.env['product.product'].browse(product_id)

    @api.model
    def _default_deposit_account_id(self):
        return self._default_product_id().property_account_income_id

    @api.model
    def _default_deposit_taxes_id(self):
        return self._default_product_id().taxes_id

    advance_payment_method = fields.Selection([
        ('delivered', 'Invoiceable lines'),
        ('all', 'Invoiceable lines (deduct down payments)'),
        ('percentage', 'Down payment (percentage)'),
        ('fixed', 'Down payment (fixed amount)')
        ], string='What do you want to invoice?', default='delivered', required=True)
    product_id = fields.Many2one('product.product', string='Down Payment Product', domain=[('type', '=', 'service')],
        default=_default_product_id)
    count = fields.Integer(default=_count, string='# of Orders')
    # amount = fields.Float('Down Payment Amount', digits=dp.get_precision('Account'), help="The amount to be invoiced in advance, taxes excluded.")
    amount = fields.Float('Down Payment Amount', digits='Account', help="The amount to be invoiced in advance, taxes excluded.")
    deposit_account_id = fields.Many2one("account.account", string="Income Account", domain=[('deprecated', '=', False)],
        help="Account used for deposits", default=_default_deposit_account_id)
    deposit_taxes_id = fields.Many2many("account.tax", string="Customer Taxes", help="Taxes used for deposits", default=_default_deposit_taxes_id)

    @api.onchange('advance_payment_method')
    def onchange_advance_payment_method(self):
        if self.advance_payment_method == 'percentage':
            return {'value': {'amount': 0}}
        return {}

    # @api.multi
    def _create_invoice(self, test, lt_line, amount):
        inv_obj = self.env['account.invoice']
        ir_property_obj = self.env['ir.property']

        account_id = False
        if self.product_id.id:
            account_id = self.product_id.property_account_income_id.id
        if not account_id:
            inc_acc = ir_property_obj.get('property_account_income_categ_id', 'product.category')
            account_id = test.fiscal_position_id.map_account(inc_acc).id if inc_acc else False
        if not account_id:
            raise UserError(
                _('There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app, settings menu.') %
                (self.product_id.name,))

        if self.amount <= 0.00:
            raise UserError(_('The value of the down payment amount must be positive.'))
        if self.advance_payment_method == 'percentage':
            amount = test.amount_untaxed * self.amount / 100
            name = _("Down payment of %s%%") % (self.amount,)
        else:
            amount = self.amount
            name = _('Down Payment')
        if test.fiscal_position_id and self.product_id.taxes_id:
            tax_ids = test.fiscal_position_id.map_tax(self.product_id.taxes_id).ids
        else:
            tax_ids = self.product_id.taxes_id.ids

        invoice = inv_obj.create({
            'name': test.client_order_ref or test.name,
            'origin': test.name,
            'move_type': 'out_invoice',
            'reference': False,
            'account_id': test.partner_id.property_account_receivable_id.id,
            'partner_id': test.partner_invoice_id.id,
            'partner_shipping_id': test.partner_shipping_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': name,
                'origin': test.name,
                'account_id': account_id,
                'price_unit': amount,
                'quantity': 1.0,
                'discount': 0.0,
                'uom_id': self.product_id.uom_id.id,
                'product_id': self.product_id.id,
                'sale_line_ids': [(6, 0, [lt_line.id])],
                'invoice_line_tax_ids': [(6, 0, tax_ids)],
                'account_analytic_id': test.project_id.id or False,
            })],
            'currency_id': test.pricelist_id.currency_id.id,
            'payment_term_id': test.payment_term_id.id,
            'fiscal_position_id': test.fiscal_position_id.id or test.partner_id.property_account_position_id.id,
            'team_id': test.team_id.id,
            'comment': test.note,
        })
        invoice.compute_taxes()
        invoice.message_post_with_view('mail.message_origin_link',
                    values={'self': invoice, 'origin': test},
                    subtype_id=self.env.ref('mail.mt_note').id)
        return invoice

    def create_invoices(self):
        test_orders = self.env['lab.tests'].browse(self._context.get('active_ids', []))

        if self.advance_payment_method == 'delivered':
            test_orders.action_invoice_create()
        elif self.advance_payment_method == 'all':
            test_orders.action_invoice_create(final=True)
        else:
            if not self.product_id:
                vals = self._prepare_deposit_product()
                self.product_id = self.env['lab.tests'].create(vals)
                self.env['ir.values'].sudo().set_default('sale.config.settings', 'deposit_product_id_setting', self.product_id.id)

            tests_line_obj = self.env['lab.tests.line']
            for test in test_orders:
                if self.advance_payment_method == 'percentage':
                    amount = test.amount_untaxed * self.amount / 100
                else:
                    amount = self.amount
                if self.product_id.invoice_policy != 'order':
                    raise UserError(_('The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
                if self.product_id.type != 'service':
                    raise UserError(_("The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
                if test.fiscal_position_id and self.product_id.taxes_id:
                    tax_ids = test.fiscal_position_id.map_tax(self.product_id.taxes_id).ids
                else:
                    tax_ids = self.product_id.taxes_id.ids
                lt_line = tests_line_obj.create({
                    'name': _('Advance: %s') % (time.strftime('%m %Y'),),
                    'price_unit': amount,
                    'product_uom_qty': 0.0,
                    'order_id': test.id,
                    'discount': 0.0,
                    'product_uom': self.product_id.uom_id.id,
                    'product_id': self.product_id.id,
                    'tax_id': [(6, 0, tax_ids)],
                })
                self._create_invoice(test, lt_line, amount)
        if self._context.get('open_invoices', False):
            return test_orders.action_view_invoice()
        return {'type': 'ir.actions.act_window_close'}

    def _prepare_deposit_product(self):
        return {
            'name': 'Down payment',
            'type': 'service',
            'invoice_policy': 'order',
            'property_account_income_id': self.deposit_account_id.id,
            'taxes_id': [(6, 0, self.deposit_taxes_id.ids)],
        }