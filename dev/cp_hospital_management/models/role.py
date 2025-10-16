# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError


class Role(models.Model):
    _name = "role.data"
    _description = "Role Data"
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    name = fields.Char('Name',tracking=True)
    type = fields.Selection([('doc','Doctor'),('nurse','Nurse')],string='Type',tracking=True)
    nurse_id = fields.Many2one('hr.employee','Nurse',tracking=True)
    doc_procedure_id = fields.Many2one('procedure',string='Doctor Role',tracking=True)
    nurse_procedure_id = fields.Many2one('procedure',string='Nurse Role',tracking=True)
    is_surgeon = fields.Boolean('Is Surgeon',copy=False,tracking=True)
    not_available = fields.Boolean('N/A',copy=False,tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(Role, self).create(vals_list)
        for res in records:
            if res.name:
                data = self.search([('name', '=ilike', res.name), ('id', '!=', res.id)])
                if data:
                    raise UserError('Already role exists in this name')
        return records

    def write(self, vals):
        res = super(Role, self).write(vals)
        if 'name' in vals and self.name:
             data = self.search([('name', '=ilike', self.name), ('id', '!=', self.id)])
             if data:
                 raise UserError('Already role exists in this name')
        return res


    # @api.model
    # def create(self , vals):
    #     res = super(Role,self).create(vals)
    #     if res.name:
    #         data = self.env['role.data'].search([('name','=ilike',res.name),('id', '!=', res.id)])
    #         if data:
    #             raise UserError('Already role exists in this name')
    #     return res

    # def write(self, vals):
    #     res = super(Role,self).write(vals)
    #     if self.name:
    #         data = self.env['role.data'].search([('name','=ilike',self.name),('id', '!=', self.id)])
    #         if data:
    #             raise UserError('Already role exists in this name')
    #     return res























