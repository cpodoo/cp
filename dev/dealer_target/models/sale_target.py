# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from collections import defaultdict

class SalesTarget(models.Model):
    _name = 'sales.target'
    _description = 'Sales Target'
    _order = 'id desc'
    _rec_name = 'name'

    # Fields
    name = fields.Char(string="Reference", readonly=True, default=lambda self: _('New'))
    salesperson_id = fields.Many2one('res.users', string='Salesperson')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    target_achieve = fields.Selection([
        ('sale_order_confirm', 'Sale Order Confirmed'),
        ('delivery_order_done', 'Delivery Order Done'),
        ('invoice_created', 'Invoice Created'),
        ('invoice_paid', 'Invoice Paid'),
    ], string='Target Achieve')
    target = fields.Integer(string='Target')
    difference = fields.Integer(string='Difference', compute='_compute_difference', store=True)
    achieve = fields.Integer(string='Achieve')
    achieve_percentage = fields.Float(string='Achieve Percentage', compute='_compute_achieve_percentage', store=True)
    responsible_salesperson_id = fields.Many2one('res.users', string='Responsible Salesperson')

    # State Field
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('canceled', 'Canceled'),
    ], string='Status', default='draft', readonly=True)

    # Computed Methods
    @api.depends('target', 'achieve')
    def _compute_difference(self):
        for record in self:
            record.difference = record.target - record.achieve

    @api.depends('target', 'achieve')
    def _compute_achieve_percentage(self):
        for record in self:
            if record.target != 0:
                record.achieve_percentage = (record.achieve / record.target) * 100
            else:
                record.achieve_percentage = 0

    # Computed field to fetch products based on target_achieve
    product_order_lines = fields.One2many('sales.target.line', 'target_id', string='Product Order Lines', compute='_compute_product_order_lines', store=True)

    @api.depends('salesperson_id', 'start_date', 'end_date', 'target_achieve')
    def _compute_product_order_lines(self):
        for record in self:
            product_lines = []
            if record.salesperson_id and record.start_date and record.end_date:
                if record.target_achieve == 'sale_order_confirm':
                    sale_orders = self.env['sale.order'].search([
                        ('user_id', '=', record.salesperson_id.id),
                        ('state', '=', 'sale'),
                        ('date_order', '>=', record.start_date),
                        ('date_order', '<=', record.end_date),
                    ])
                    product_count = defaultdict(int)
                    for order in sale_orders:
                        for line in order.order_line:
                            product_count[line.product_id.id] += 1
                    product_lines = [(0, 0, {'product_id': pid, 'sale_count': count}) for pid, count in
                                     product_count.items()]

                elif record.target_achieve == 'delivery_order_done':
                    stock_pickings = self.env['stock.picking'].search([
                        ('user_id', '=', record.salesperson_id.id),
                        ('state', '=', 'done'),
                        ('date_done', '>=', record.start_date),
                        ('date_done', '<=', record.end_date),
                    ])
                    product_ids = {move.product_id.id for picking in stock_pickings for move in picking.move_ids if
                                   move.state == 'done'}
                    product_lines = [(0, 0, {'product_id': pid}) for pid in product_ids]

                elif record.target_achieve == 'invoice_created':
                    invoices = self.env['account.move'].search([
                        ('invoice_user_id', '=', record.salesperson_id.id),
                        ('state', '=', 'posted'),
                        ('invoice_date', '>=', record.start_date),
                        ('invoice_date', '<=', record.end_date),
                    ])
                    product_quantities = defaultdict(float)
                    for invoice in invoices:
                        for line in invoice.invoice_line_ids:
                            if line.product_id:
                                product_quantities[line.product_id.id] += line.quantity
                    product_lines = [(0, 0, {'product_id': pid, 'invoice_quantity': qty}) for pid, qty in
                                     product_quantities.items()]

                elif record.target_achieve == 'invoice_paid':
                    invoices = self.env['account.move'].search([
                        ('invoice_user_id', '=', record.salesperson_id.id),
                        ('state', '=', 'posted'),
                        ('payment_state', '=', 'paid'),
                        ('invoice_date', '>=', record.start_date),
                        ('invoice_date', '<=', record.end_date),
                    ])
                    product_quantities = defaultdict(float)
                    for invoice in invoices:
                        for line in invoice.invoice_line_ids:
                            if line.product_id:
                                product_quantities[line.product_id.id] += line.quantity
                    product_lines = [(0, 0, {'product_id': pid, 'paid_quantity': qty}) for pid, qty in
                                     product_quantities.items()]

            # Ensure the field is always assigned, even if empty
            record.update({'product_order_lines': product_lines})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sales.target') or _("New")
        return super().create(vals_list)

    def action_send_email(self):
        self.ensure_one()  # Ensure only one record is processed

        # Get the responsible salesperson's email
        email_to = self.responsible_salesperson_id.email
        if not email_to:
            raise UserError("The responsible salesperson does not have an email address configured.")
        # Email subject and body
        subject = f"Sales Target Update: {self.name}"
        body = f"""
           <p>Hello {self.responsible_salesperson_id.name},</p>
           <p>This is an update regarding the sales target <strong>{self.name}</strong>.</p>
           <p>Details:</p>
           <ul>
               <li>Start Date: {self.start_date}</li>
               <li>End Date: {self.end_date}</li>
               <li>Target: {self.target}</li>
               <li>Achieved: {self.achieve}</li>
               <li>Achievement Percentage: {self.achieve_percentage}%</li>
           </ul>
           <p>Thank you,</p>
           <p>Your Sales Team</p>
           """

        # Send the email
        self.env['mail.mail'].create({
            'subject': subject,
            'body_html': body,
            'email_to': email_to,
            'email_from': self.env.user.email or 'noreply@example.com',
        }).send()

        # Log the email as a message in the chatter
        self.message_post(body=f"Email sent to {email_to} with subject: {subject}")

        return True

    def action_open(self):
        for record in self:
            record.state = 'open'

    def action_close(self):
        for record in self:
            record.state = 'closed'

    def action_cancel(self):
        for record in self:
            record.state = 'canceled'

    def action_confirm(self):
        if self.target <= 0:
            raise UserError("Target must be greater than 0.")


class SalesTargetLine(models.Model):
    _name = 'sales.target.line'
    _description = 'Sales Target Line'

    target_id = fields.Many2one('sales.target', string='Target')
    product_id = fields.Many2one('product.product', string='Product')
    sale_count = fields.Integer(string='Sale Count')  # Number of times the product was sold
    invoice_quantity = fields.Float(string='Invoice Quantity')  # Total quantity in invoices
    paid_quantity = fields.Float(string='Paid Quantity')  # Total quantity in paid invoices
