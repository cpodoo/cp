from odoo import api, fields, models

class real_estate(models.Model):
    _name = 'test.model'
    _description = 'Test Model'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date()
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="No. of Bedrooms")
    living_area = fields.Integer(string="Size of living area")
    garage = fields.Boolean(string="Garage", default=True)
    garden = fields.Boolean(string="Garden", default=True)
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'),
                                           ('west', 'West')], string="Garden Orientation")
    create_date = fields.Datetime(string="Created On", readonly=True)
    create_uid = fields.Many2one('res.users', string="Created By", readonly=True)
    write_date = fields.Datetime(string="Last Updated On", readonly=True)
    write_uid = fields.Many2one('res.users', string="Last Updated By", readonly=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    def action_under_review(self):
        for rec in self:
            rec.state = 'under_review'

    def action_approve(self):
        for rec in self:
            rec.state = 'approved'

    def action_sold(self):
        for rec in self:
            rec.state = 'sold'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_set_to_draft(self):
        for rec in self:
            rec.state = 'draft'