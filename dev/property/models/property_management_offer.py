from odoo import models, fields, api
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class PropertyManagementOffer(models.Model):
    _name = "property.management.offer"
    _description = "Property Management Offer"
    _order = "offer_price asc"

    offer_price = fields.Float(string="Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    expected_start_date = fields.Date(string="Expected Start Date",compute="_compute_expected_start_date")
    offer_deadline = fields.Date(
        string="Deadline",
        compute="_compute_offer_deadline",
        inverse="_inverse_offer_deadline",
    )
    validity = fields.Integer(string="Validity", default=7)
    property_id = fields.Many2one(
        "property.management", required=True, string="Constrcution Id"
    )

    _sql_constraints = [
        (
            "positive_price",
            "CHECK(offer_price > 0)",
            "An offer price must be strictly positive",
        ),
    ]
    @api.model
    def create(self, vals):
        offer = super().create(vals)
        offer.property_id.state="offer_received"
        existing_offers = self.search(
            [("property_id", "=", offer.property_id.id), ("id", "!=", offer.id)]
        )
        for record in existing_offers:
            if offer.offer_price > record.offer_price:
                raise ValidationError("Offer Price should be smaller than existing offers")
        return offer

    def unlink(self):
        property_ids = self.mapped("property_id")
        super().unlink()
        for record in property_ids:
            remaining_offers = self.env["property.management.offer"].search(
                [("property_id", "=", record.id)]
            )
            if not remaining_offers:
                record.state = "new"

    @api.depends("create_date", "validity")
    def _compute_offer_deadline(self):
        for record in self:
            if record.create_date:
                record.offer_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.offer_deadline = date.today() + timedelta(days=record.validity)

    def _inverse_offer_deadline(self):
        for record in self:
            if record.create_date and record.offer_deadline:
                record.validity = (fields.Date.from_string(record.offer_deadline) - fields.Date.from_string(record.create_date)).days

    @api.depends("offer_deadline")
    def _compute_expected_start_date(self):
        for record in self:
            if record.offer_deadline:
                record.expected_start_date = record.offer_deadline + timedelta(days=7)

    def property_management_offer_action_accept(self):
        for record in self:
            if record.property_id.contractor_budget != 0.0:
                raise UserError("Can not accept more than one offer")
            else:
                property_id = record.property_id
                property_offers = self.env["property.management.offer"].search(
                    [
                        ("id", "!=", record.id),
                        ("property_id", "=", property_id.id),
                    ]
                )
                property_offers.write({"status": "refused"})
                record.status = "accepted"
                property_id.state = "offer_accepted"
                property_id.contractor_budget = record.offer_price
                property_id.contractor_id = record.partner_id
                property_id.start_date = record.expected_start_date
                property_id.end_date = record.expected_start_date + timedelta(days = 30 * property_id.tenure)
        return True

    def property_management_offer_action_refuse(self):
        for record in self:
            record.status = "refused"
            record.property_id.contractor_budget = 0.0
            record.property_id.contractor_id = False
            record.property_id.start_date=""
            record.property_id.end_date = ""
        return True
