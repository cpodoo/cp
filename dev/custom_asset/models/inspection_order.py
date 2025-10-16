from odoo import models, fields, api
from datetime import datetime

class InspectionOrder(models.Model):
    _name = 'inspection.order'
    _description = 'Inspection Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _order = 'inspection_order_no desc'

    # Main Fields
    inspection_order_no = fields.Char(
        string='Inspection Order No',
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )

    current_location = fields.Char(
        string='Current Location',
        help='Taken from inventory as per current warehouse name'
    )
    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Warehouse',
        tracking=True
    )
    warehouse_address = fields.Char(
        related='warehouse_id.partner_id.contact_address_complete',
        string='Warehouse Address',
        readonly=True
    )

    current_reading = fields.Integer(
        string='Current Reading',
        tracking=True
    )

    scheduled_date = fields.Date(
        string='Scheduled Date',
        required=True,
        tracking=True
    )

    assigned_to = fields.Many2one(
        'hr.employee',
        string='Assigned To',
        required=True,
        tracking=True
    )

    owner_id = fields.Many2one(
        'res.users',
        string='Owner',
        default=lambda self: self.env.user,
        tracking=True
    )

    planned_date = fields.Date(
        string='Planned Date',
        tracking=True
    )

    actual_date = fields.Date(
        string='Actual Date',
        tracking=True
    )
    remarks_note = fields.Html(
        string='Remarks and Findings',
        help='Detailed notes about the inspection'
    )
    # Stage
    stage = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Stage', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('inspection_order_no', 'New') == 'New':
            vals['inspection_order_no'] = self.env['ir.sequence'].next_by_code('inspection.order') or '/'
        return super().create(vals)

    def action_schedule(self):
        self.stage = 'scheduled'

    def action_start_inspection(self):
        self.stage = 'in_progress'
        self.actual_date = fields.Date.today()

    def action_complete_inspection(self):
        self.stage = 'completed'

    def action_cancel_inspection(self):
        self.stage = 'cancelled'