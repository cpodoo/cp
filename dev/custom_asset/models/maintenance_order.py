from odoo import models, fields, api
from datetime import datetime


class MaintenanceOrder(models.Model):
    _name = 'maintenance.order'
    _description = 'Maintenance Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _order = 'maintenance_order_no desc'

    # Main Fields
    maintenance_order_no = fields.Char(
        string='Maintenance Order No',
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
    # Priority
    priority = fields.Selection([
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], string='Priority', default='normal', tracking=True)

    # Maintenance Type
    maintenance_type = fields.Selection([
        ('preventive', 'Preventive'),
        ('corrective', 'Corrective'),
        ('emergency', 'Emergency')
    ], string='Maintenance Type', default='preventive', tracking=True)

    # Cost Information
    estimated_cost = fields.Float(
        string='Estimated Cost',
        tracking=True
    )

    actual_cost = fields.Float(
        string='Actual Cost',
        tracking=True
    )

    # Remarks and Findings
    remarks_note = fields.Html(
        string='Remarks and Findings',
        help='Detailed notes about the maintenance'
    )
    # Task List
    task_ids = fields.One2many(
        'maintenance.task',
        'maintenance_order_id',
        string='Tasks'
    )
    # Stage
    stage = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Stage', default='draft', tracking=True)

    # Computed Fields
    task_count = fields.Integer(
        string='Task Count',
        compute='_compute_task_count'
    )
    @api.model
    def create(self, vals):
        if vals.get('maintenance_order_no', 'New') == 'New':
            vals['maintenance_order_no'] = self.env['ir.sequence'].next_by_code('maintenance.order') or '/'
        return super().create(vals)

    def action_schedule(self):
        self.stage = 'scheduled'

    def action_start_maintenance(self):
        self.stage = 'in_progress'
        self.actual_date = fields.Date.today()

    def action_complete_maintenance(self):
        self.stage = 'completed'

    def action_cancel_maintenance(self):
        self.stage = 'cancelled'

class MaintenanceTask(models.Model):
    _name = 'maintenance.task'
    _description = 'Maintenance Task'
    _order = 'sequence, id'

    maintenance_order_id = fields.Many2one(
        'maintenance.order',
        string='Maintenance Order',
        required=True,
        ondelete='cascade'
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10
    )

    name = fields.Char(
        string='Task Name',
        required=True
    )

    description = fields.Text(
        string='Description'
    )

    product_id = fields.Many2one(
        'product.product',
        string='Product/Part'
    )

    quantity = fields.Float(
        string='Quantity',
        default=1.0
    )

    activity_type = fields.Selection([
        ('repair', 'Repair'),
        ('replace', 'Replace'),
        ('check', 'Check'),
        ('clean', 'Clean'),
        ('lubricate', 'Lubricate')
    ], string='Activity Type', required=True)

    status = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='pending')

    assigned_to = fields.Many2one(
        'hr.employee',
        string='Assigned To'
    )

    estimated_hours = fields.Float(
        string='Estimated Hours'
    )

    actual_hours = fields.Float(
        string='Actual Hours'
    )

    remarks = fields.Text(
        string='Remarks'
    )

    def action_start_task(self):
        self.status = 'in_progress'

    def action_complete_task(self):
        self.status = 'completed'

    def action_cancel_task(self):
        self.status = 'cancelled'
