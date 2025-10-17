from odoo import fields, models, api
from odoo.exceptions import ValidationError

class PropertyManagementPayment(models.Model):
    _name = "property.management.payment"
    _description = "Property Management Payment"

    name = fields.Char(
        string="Payment Reference",
        required=True,
        readonly=True,
        compute="_compute_name",
    )
    amount = fields.Float(string="Amount", required=True)
    account_number = fields.Integer(string="Account Number", required=True)
    date = fields.Date(
        string="Payment Date", default=fields.Date.today(), readonly=True
    )
    property_id = fields.Many2one(
        "property.management", string="property", required=True
    )

    # _sql_constraints = [
    #     (
    #         "check_payment_amount",
    #         "CHECK(amount > property_id.pending_amount)",
    #         "Payment amount cannot exceed pending amount.",
    #     ),
    # ]

    @api.constrains("amount")
    def _check_amount(self):
        for payment in self:
            if payment.amount > payment.property_id.pending_amount:
                raise ValidationError("Payment amount cannot exceed pending amount.")

    @api.depends("property_id.contractor_id")
    def _compute_name(self):
        for record in self:
            if record.property_id.contractor_id:
                record.name = record.property_id.contractor_id.name
