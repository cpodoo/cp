from odoo import models, fields, api

class MrCustom(models.Model):
    _name = 'mr.custom'
    _description = 'Material Requisition Custom'

    name = fields.Char(string='Order Number', required=True, copy=False, readonly=True, default='New')
    purpose = fields.Text(string="Purpose")

    request_raised_by_id = fields.Many2one('res.partner', string='Request Raised By')
    department = fields.Char(string='Department')
    job_position = fields.Char(string='Job Position')
    reporting_manager_id = fields.Many2one('res.users', string='Reporting Manager')
    destination_location_id = fields.Many2one('stock.warehouse', string='Destination Location')

    request_raised_for_id = fields.Many2one('res.partner', string='Request Raised For')
    indent_date = fields.Datetime(string='Indent Date', default=fields.Datetime.now)
    required_date = fields.Datetime(string='Required Date')
    requirement = fields.Selection([
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
    ], default = 'normal', string='Requirement')
    notes = fields.Text(string="Additional Information")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval', 'Waiting 3rd Level Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('done', 'Done'),
        ('delivered', 'Delivered'),
    ], string="Status", default="draft", tracking=True)

    ribbon_state = fields.Char(string="Ribbon State", compute="_compute_ribbon_state", store=True)

    # Workflow Actions
    def action_submit(self):
        for rec in self:
            rec.status = 'waiting_approval'

    def action_approve(self):
        for rec in self:
            rec.status = 'approved'

    def action_reject(self):
        for rec in self:
            rec.status = 'rejected'

    def action_done(self):
        for rec in self:
            rec.status = 'done'

    def action_delivered(self):
        for rec in self:
            rec.status = 'delivered'

    @api.depends('status')
    def _compute_ribbon_state(self):
        for rec in self:
            if rec.status == 'waiting_approval':
                rec.ribbon_state = 'Waiting 3rd Level Approval'
            elif rec.status == 'approved':
                rec.ribbon_state = 'Approved'
            elif rec.status == 'rejected':
                rec.ribbon_state = 'Rejected'
            elif rec.status == 'delivered':
                rec.ribbon_state = 'Delivered'
            elif rec.status == 'done':
                rec.ribbon_state = 'Done'
            else:
                rec.ribbon_state = ''

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            fiscal_year = self._get_fiscal_year()
            sequence = self.env['ir.sequence'].next_by_code('mr.custom') or '00001'
            vals['name'] = f'MR/{fiscal_year}/{sequence}'
        return super(MrCustom, self).create(vals)

    def _get_fiscal_year(self):
        today = fields.Date.context_today(self)
        year = today.year
        if today.month >= 4:  # Assuming fiscal year starts in April
            return f'{str(year)[-2:]}-{str(year + 1)[-2:]}'
        else:
            return f'{str(year - 1)[-2:]}-{str(year)[-2:]}'


    product_line_ids = fields.One2many('mr.custom.line', 'mr_custom_id', string='Requested Products')

class MrCustomLine(models.Model):
    _name = 'mr.custom.line'
    _description = 'Material Requisition Line'

    mr_custom_id = fields.Many2one('mr.custom', string='Material Requisition', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_qty = fields.Float(string='Quantity', required=True, default=1.0)
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    on_hand_qty = fields.Float(string='On-Hand Quantity', compute='_compute_on_hand_qty', store=True)
    short_close = fields.Boolean(string='Short Close')

    @api.depends('product_id')
    def _compute_on_hand_qty(self):
        for line in self:
            if line.product_id:
                location = line.mr_custom_id.destination_location_id.lot_stock_id.id if line.mr_custom_id.destination_location_id else False
                line.on_hand_qty = line.product_id.with_context(location=location).qty_available
            else:
                line.on_hand_qty = 0.0

