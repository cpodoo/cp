# -*- coding: utf-8 -*-

from odoo import models, fields

class DoctorMembership(models.Model):
    _name = "doctor.membership"
    _description = "Doctor Membership"

    membership_number = fields.Char('Membership Number',tracking=True)
    type_of_membership = fields.Char('Type of membership',tracking=True)
    valid_till  = fields.Date('Valid till',tracking=True)
    other_remarks  = fields.Char('Other remarks',tracking=True)
    membership_attach = fields.Many2many('ir.attachment','membership_attach_rel','membership_id','membership_attach_id',string="Attachments",tracking=True)
    doctor_id = fields.Many2one('res.partner',string='Doctor',tracking=True)