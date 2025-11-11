# -*- coding: utf-8 -*-

from odoo import models, fields , api

class DoctorProcedures(models.Model):
    _name = "doctor.procedures"
    _description = "Doctor Procedures"

    procedure_id = fields.Many2one('procedure','Procedure',tracking=True)
    avg_time = fields.Float('Average Time',tracking=True)
    avg_time_actual = fields.Float('Average Time',tracking=True)
    min_time = fields.Float('Min Time',tracking=True)
    max_time = fields.Float('Max Time',tracking=True)
    doctor_id = fields.Many2one('res.partner','Doctor',tracking=True)

    @api.onchange('procedure_id')
    def get_procdures_data(self):
        if self.procedure_id:
            self.avg_time = self.procedure_id.avg_time
            self.avg_time_actual = self.procedure_id.avg_time_actual
            self.min_time = self.procedure_id.min_time
            self.max_time = self.procedure_id.max_time