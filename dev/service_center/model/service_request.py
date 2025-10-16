from odoo import fields, models, api,_
from datetime import datetime
from odoo.exceptions import ValidationError



class ServiceRequest(models.Model):
    _name = "service.request"
    _inherit = ['mail.thread']
    _rec_name = 'sequence'

    sequence = fields.Char(string="Sequence", tracking=True, readonly=True,default=lambda self: _('New'))
    priority = fields.Selection(
        [('0', 'Normal'), ('1', 'Urgent')], 'Priority', default='0', index=True)
    name = fields.Char(string="Customer Name", store=True, required=True)
    date = fields.Datetime(string="Request Date", default=fields.Datetime.now, copy=False)
    # type=fields.Selection([('software','Software'),('hardware','Hardware')],string="Type")
    is_software = fields.Boolean(string='Software')
    is_hardware = fields.Boolean(string='Hardware')
    is_other = fields.Boolean(string='Other')
    status = fields.Selection([('new', 'New'),
                               ('process', 'Process'),
                               ('cancel', 'Cancel'),
                               ('scrap', 'Scrap'),
                               ('done', 'Done'),
                               ], string="Status", default='new', copy=False, tracking=True)
    start_date = fields.Date(string="Start Date", copy=False, noupadate="1")
    end_date = fields.Date(string="End Date", copy=False)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone", size=10)

    total_amount = fields.Float(string="Total Amount", compute='_compute_total')
    request_line = fields.One2many('service.request.line', 'request_id', string="Request Line", required=True)
    notes = fields.Text(string="Remarks")
    duration = fields.Float(string="Duration (days)", compute="_compute_duration", store=True, copy=False)
    time = fields.Float(string="time", store=True)
    file = fields.Binary(string="File", store=True)
    planning_month = fields.Float(string="Planning Month", store=True)

    progress = fields.Float(string="Progress", compute="_compute_progress", store=True)

    @api.depends('status')
    def _compute_progress(self):
        for record in self:
            if record.status == 'new':
                record.progress = 0
            elif record.status == 'process':
                record.progress = 50
            elif record.status in ['cancel', 'scrap']:
                record.progress = 100
            elif record.status == 'done':
                record.progress = 100

    def preview_service_request_report(self):

        return {
            'type': 'ir.actions.act_url',
            'url': f'/report/pdf/service_center.custom_sr_pdf_report/{self.id}',
            'target': 'new',
        }

    @api.model
    def create(self, vals):
        # result=super(ServiceRequest,self).create(vals)
        vals['sequence'] = self.env['ir.sequence'].next_by_code('service_request')

        return super(ServiceRequest, self).create(vals)

    @api.model
    def unlink(self, vals):
        if self.status != 'done':
            raise ValidationError("You can not delete without state done")
        return super(ServiceRequest, self).unlink(vals)

    # @api.model
    # def write(self,vals):
    #     if self.start_date > self.end_date:
    #         raise ValidationError("Date must less than Start Date")
    #     return super(ServiceRequest,self).write(vals)

    @api.model
    def write(self, values):
        if self.start_date > self.end_date:
            print("write")
            raise ValidationError("Date must less than Start Date")
        result = super(ServiceRequest, self).write(values)
        return result

    # @api.constrains('start_date','end_date')
    # def _check_dates(self):
    #     for rec in self:
    #         if rec.start_date > rec.end_date:
    #             raise ValidationError("Date must less than Start Date")

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                start = fields.Date.from_string(record.start_date)
                end = fields.Date.from_string(record.end_date)
                duration = (end - start).days
                record.duration = duration
            else:
                record.duration = 0.0

    @api.depends('request_line.price')
    def _compute_total(self):
        for i in self:
            i.total_amount = sum(line.price for line in i.request_line)

    def in_process(self):
        for a in self:
            a.status = 'process'

    def cancel(self):
        for a in self:
            a.status = 'cancel'

    def scrap(self):
        for a in self:
            a.status = 'scrap'

    def done(self):
        for a in self:
            a.status = 'done'

    def duplicate_record(self):
        for record in self:
            duplicate = record.copy()
            duplicatelines = record.request_line.copy()
            duplicatelines.request_id = duplicate.id
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'service.request',
                'views': [(duplicate.id, 'form'), (False, 'tree')],
                'res_id': self.id,
                'target': 'new'
            }

    def send_email(self):
        mail_template = self.env.ref("service_center.service_request_mail_temp")
        mail_template.send_mail(self.id, force_send=True)

    # def action_open_sale_order_action(self):
    #     for record in self:

    # return {
    #     'type': 'ir.actions.act_window',
    #     'view_type': 'form',
    #     'view_mode': 'form',
    #     'res_model': 'service.request.from',
    #     'views': [(self.id, 'form'), (False, 'tree')],
    #     'res_id': self.id,
    #     'target': 'new'
    # }

    def action_open_product_catalog(self):
        return {
            'name': 'Product Catalog',
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban',
            'res_model': 'product.product',
            'views': [(self.env.ref('product.product_view_kanban_catalog').id, 'kanban')],
            'target': 'new',
        }


class ServiceRequestLine(models.Model):
    _name = "service.request.line"

    request_id = fields.Many2one('service.request', string="Request Id", copy=False)
    item_id = fields.Many2one('product.item', string="Product", required=True)
    description = fields.Char(string='Description')
    brand_id = fields.Many2one(string="Brand", related='item_id.brand_id')
    repair_status = fields.Selection([('done', 'Done'), ('inprocess', 'In Process')], string="Repair Status",
                                     default='inprocess')
    price = fields.Float(string="Repair Price", copy=False)
    image = fields.Image(string="Image", related="item_id.image")
    sensitive_items = fields.Boolean(string="Sensitive Items", store=True)


