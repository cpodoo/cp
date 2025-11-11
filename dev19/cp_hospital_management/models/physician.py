# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    speciality_id = fields.Many2one('physician.speciality', string='Speciality')
    degree_ids = fields.Many2many('physician.degree', string='Degrees')
    grad_inst_id = fields.Many2one('res.partner', string='Graduation Institute', domain="[('is_company', '=', True)]")
    is_pharmacist = fields.Boolean('Is Pharmacist')
    consult_type = fields.Selection([
        ('in_person', 'In-Person'),
        ('online', 'Online'),
    ], string='Consultation Type')
    consult_charge = fields.Float('Consultation Charge')
    licence_id = fields.Char('License ID')
    resp = fields.Text('Responsibilities')
    work_location = fields.Char('Working Location')
    app_count = fields.Integer(string='Appointments Count', compute='_compute_appointment_count')
    prescription_count = fields.Integer(string='Prescription Count', compute='_compute_prescription_count')
    app_count=fields.Float(compute='_compute_appointments')
    prescription_count=fields.Float(compute='_compute_prescriptions')
    is_physician = fields.Boolean('Is a Physician')

    def _compute_appointments(self):
        Appointment = self.env['appointment']
        self.app_count = Appointment.search_count([('doctor.id', '=', self.id)])

    def _compute_prescriptions(self):
        Prescription = self.env['prescription']
        self.prescription_count = Prescription.search_count([('doctor.id', '=', self.id)])

class PhysicianSpeciality(models.Model):
    _name = 'physician.speciality'
    _description = "Physician Speciality"

    name = fields.Char("Description", required=True)
    code = fields.Char("")


class PhysicianDegree(models.Model):
    _name = 'physician.degree'
    _description = "Physician Degree"

    name = fields.Char("Degree", required=True)
    full_form = fields.Char("Full Name")