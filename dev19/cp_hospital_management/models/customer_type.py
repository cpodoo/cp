# -*- coding: utf-8 -*-

from odoo import models, fields ,api
from odoo.exceptions import UserError

class CustomerType(models.Model):
    _name = "customer.type"
    _description = "Customer Type"
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    name = fields.Char(string ='Type',tracking=True)

    # @api.model
    # def create(self , vals):
    #     res = super(CustomerType,self).create(vals)
    #     if res.name:
    #         data = self.env['customer.type'].search([('name','=ilike',res.name),('id', '!=', res.id)])
    #         if data:
    #             raise UserError('Already role exists in this name')
    #     return res

    # def write(self, vals):
    #     res = super(CustomerType,self).write(vals)
    #     if self.name:
    #         data = self.env['role.data'].search([('name','=ilike',self.name),('id', '!=', self.id)])
    #         if data:
    #             raise UserError('Already role exists in this name')
    #     return res

    @api.model_create_multi
    def create(self, vals_list):
        records = super(CustomerType, self).create(vals_list)
        for res in records:
            if res.name:
                data = self.search([('name', '=ilike', res.name), ('id', '!=', res.id)])
                if data:
                    raise UserError('Already customer type exists with this name')
        return records

    def write(self, vals):
        res = super(CustomerType, self).write(vals)
        if 'name' in vals and self.name: # Check if name is being changed
            data = self.search([('name', '=ilike', self.name), ('id', '!=', self.id)])
            if data:
                raise UserError('Already customer type exists with this name')
        return res