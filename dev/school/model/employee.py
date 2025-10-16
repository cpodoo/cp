from odoo import models, fields

class EmployeeTraining(models.Model):
    _name = 'hr.employee.training'

    name = fields.Char(string='Training Name')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    training_date = fields.Date(string='Training Date')
    trainer = fields.Char(string='Trainer')
