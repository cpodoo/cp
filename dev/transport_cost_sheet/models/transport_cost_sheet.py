from odoo import models, fields, api


class TransportCostSheet(models.Model):
    _name = 'transport.cost.sheet'
    _description = 'Transport Cost Sheet'
    _rec_name = 'name'  # Optional: Display name in views

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')

    client_name = fields.Many2one('res.partner', string="Client Name")

    cargo_origin = fields.Char()
    cargo_destination = fields.Char()
    cargo_distance = fields.Float()
    cargo_transit_time = fields.Float()

    mob_origin = fields.Char()
    mob_destination = fields.Char()
    mob_distance = fields.Float()
    mob_transit_time = fields.Float()

    demob_origin = fields.Char()
    demob_destination = fields.Char()
    demob_distance = fields.Float()
    demob_transit_time = fields.Float()

    @api.depends('cargo_distance', 'mob_distance', 'demob_distance')
    def _compute_totals(self):
        for rec in self:
            rec.total_distance = rec.cargo_distance + rec.mob_distance + rec.demob_distance


    free_waiting_time = fields.Char()
    km_run_per_day = fields.Float()
    total_distance = fields.Float(compute="_compute_totals", store=True)
    total_time = fields.Char(compute="_compute_total_time", store=True)

    @api.depends('cargo_transit_time', 'mob_transit_time', 'demob_transit_time')
    def _compute_total_time(self):
        for rec in self:
            rec.total_time = rec.cargo_transit_time + rec.mob_transit_time + rec.demob_transit_time

    length_mm = fields.Float(string="Length (MM)")
    width_mm = fields.Float(string="Width (MM)")
    height_mm = fields.Float(string="Height (MM)")
    weight_mt = fields.Float(string="Weight (MT)")

    client_drawing = fields.Boolean()
    loading_drawing = fields.Boolean()
    lashing_drawing = fields.Boolean()
    stability_calc = fields.Boolean()

    puller_make = fields.Char()
    puller_type = fields.Char()
    payload_mt_1 = fields.Float(string="Payload (MT)")
    drop_deck = fields.Boolean()

    axles_no = fields.Integer()
    axle_make = fields.Char()
    payload_mt_2 = fields.Float(string="Payload (MT)")
    frame = fields.Boolean()

    route = fields.Text()
    cost_line_ids = fields.One2many('transport.cost.line', 'sheet_id', string="Cost Lines")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('transport.cost.sheet') or 'New'
        return super(TransportCostSheet, self).create(vals)

    @api.model
    def get_dashboard_data(self):
        total = self.search_count([])
        return {'total_cost_sheets': total}


class TransportCostLine(models.Model):
    _name = 'transport.cost.line'
    _description = 'Transport Cost Line'

    sheet_id = fields.Many2one('transport.cost.sheet', required=True, ondelete='cascade')
    description = fields.Char()
    category = fields.Selection([
        ('puller', 'Puller'),
        ('axles', 'Axles'),
        ('accessories', 'Accessories'),
        ('loading', 'Mob Loading'),
        ('unloading', 'Mob Unloading')
    ])
    quantity = fields.Integer()
    rate = fields.Float()
    amount = fields.Float(compute='_compute_amount', store=True)

    @api.depends('quantity', 'rate')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.quantity * rec.rate
