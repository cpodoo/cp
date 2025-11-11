# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Newborn(models.Model):
    _name = 'newborn'
    _inherit = ['mail.thread']
    _description = "Newborn"

    image=fields.Binary()
    name=fields.Char()
    mother=fields.Char(required=True)
    sex=fields.Selection([('m','Male'),('f','Female')],required=True,string="Sex")
    bdate=fields.Date("Date of Birth",required=True)
    discharged=fields.Boolean()
    doctor_in_charge=fields.Many2one('hr.employee',required=True)
    length=fields.Float()
    weight=fields.Float()
    cephalic_perimeter=fields.Float('Cephalic Perimeter(CP)')
    congenital_diseases=fields.Char()

    newborn_line = fields.One2many('newborn.line', 'newborn_id', string='Newborn Lines', copy=True)

class NewbornLine(models.Model):
    _name = 'newborn.line'
    _description = "Newborn Line"

    newborn_id = fields.Many2one('newborn', ondelete='cascade', index=True, copy=False)
    minute=fields.Float()
    apgar=fields.Float('APGAR Score')
    appearance=fields.Char()
    pulse=fields.Float()
    grimace=fields.Char()
    activity=fields.Char()
    respiration=fields.Char()