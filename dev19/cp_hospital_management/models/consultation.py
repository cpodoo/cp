# -*- coding: utf-8 -*-

from odoo import models, fields ,api
from odoo.exceptions import UserError

class Consultation(models.Model):
    _inherit = "evaluation"

    bmi = fields.Float('Body Mass Index',tracking=True)
    uom_id = fields.Many2one('uom.uom',string='Unit',tracking=True)
    doctor_id = fields.Many2one('res.partner',domain=[('is_doctor','=',True)],string='Doctor',tracking=True)

    @api.model
    def create(self , vals):
        res = super(Consultation,self).create(vals)
        print('res____________________',res,vals)
        if res.evaluation_start_date and res.evaluation_end_date:
            if res.evaluation_start_date > res.evaluation_end_date:
                raise UserError('Consultation start date should be set before end date')
        return res

    def write(self , vals):
        res = super(Consultation,self).write(vals)
        print('res____________________',self)
        if self.evaluation_start_date and  self.evaluation_end_date:
            if self.evaluation_start_date > self.evaluation_end_date:
                raise UserError('Consultation start date should be set before end date')
        return res