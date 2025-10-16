# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class Insurance(models.Model):
    _name='insurance'
    _description = "Health Insurance"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.depends('create_uid')
    def _compute_create_uid(self):
        for r in self:
            self.cus_create_uid = self.create_uid.id or 'n/a'

    def _compute_create_date(self):
        for r in self:
            self.create_date = self.create_date.id or 'n/a'        

    def _compute_write_uid(self):
        for r in self:
            self.write_uid = self.write_uid.id or 'n/a'

    def _compute_write_date(self):
        for r in self:
            self.write_date = self.write_date.id or 'n/a'
        

    name=fields.Char(string='Name', size=264,required=True,
                            help='Health Insurance Name')
    patient = fields.Many2one('res.partner', 'Patient', required=True)

    alias=fields.Char('Alias', size=64, help='Common namethat the Insurance is referred')
    insurance_code=fields.Char(size=64, string='Insurance Code', required=False)
    description=fields.Text(string='Description')
    insurance_info=fields.Text(string='Info')
    date_insurance_inclusion=fields.Date('Inclusion Date')
    date_insurance_activation=fields.Date('Activation Date')
    date_insurance_inactivation=fields.Date('Inactivation Date')
    date_insurance_suspension=fields.Date('Suspension Date')
    insurance_status= fields.Selection([('U', 'Undefined'),('A', 'Activated'),('I', 'Inactivated'),('S', 'Suspended'),],string='Status')
    state=fields.Selection([('new','New'),('revised','Revised'),('waiting','Waiting'),('okay','Okay')], 'Stage')
    cus_create_uid=fields.Char(compute='_compute_create_uid', store=True, string='Create User',readonly=True)
    create_date=fields.Datetime(compute='_compute_create_date', store=True, string='Create Date',readonly=True)
    write_uid=fields.Char(compute='_compute_write_uid', store=True,string='Write User',readonly=True)
    write_date=fields.Datetime(compute='_compute_write_date', store=True,string='Write Date',readonly=True)