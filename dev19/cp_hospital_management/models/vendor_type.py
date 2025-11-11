# -*- coding: utf-8 -*-


from odoo import models, fields ,api
from odoo.exceptions import UserError

class VendorType(models.Model):
    _name = "vendor.type"
    _description = "Vendor Type"
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    name = fields.Char('Type',tracking=True)

    @api.model_create_multi
    def create(self , vals_list):
        records = super(VendorType, self).create(vals_list)
        for res in records:
            if res.name:
                data = self.search([('name', '=ilike', res.name), ('id', '!=', res.id)])
                if data:
                    raise UserError('Already vendor type exists in this name')
        return records

    def write(self, vals):
        res = super(VendorType,self).write(vals)
        if 'name' in vals and self.name:
            data = self.search([('name', '=ilike', self.name), ('id', '!=', self.id)])
            if data:
                raise UserError('Already vendor type exists in this name')
        return res

    # @api.model
    # def create(self , vals):
    #     res = super(VendorType,self).create(vals)
    #     if res.name:
    #         data = self.env['vendor.type'].search([('name','=ilike',res.name),('id', '!=', res.id)])
    #         if data:
    #             raise UserError('Already role exists in this name')
    #     return res

    # def write(self, vals):
    #     res = super(VendorType,self).write(vals)
    #     if self.name:
    #         data = self.env['vendor.type'].search([('name','=ilike',self.name),('id', '!=', self.id)])
    #         if data:
    #             raise UserError('Already role exists in this name')
    #     return res




























