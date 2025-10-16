# -*- coding: utf-8 -*-


from odoo import api, fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    res_cust_group_1 = fields.Many2one('customer.group',string='Customer Group 1',tracking=True)
    vendor_type = fields.Many2one('vendor.type',string='Vendor Type',tracking=True)
    boolean_check = fields.Boolean('Check',copy=False,tracking=True)
    allowed_surgeon = fields.Boolean('Slot Booking Allowed',copy=False,tracking=True)
    allowed_surgeon_ids = fields.One2many('allowed.surgeon','partner_id',string='List of allowed surgeon',tracking=True)
    customer_type = fields.Many2one('customer.type',string='Customer Type',tracking=True)

    @api.onchange('allowed_surgeon')
    def add_surgeon(self):
        result = []
        if self.allowed_surgeon == True:
            surgeon_role = self.env['role.data'].search([('is_surgeon','=',True)])
            print('ro;le______________________________--',self.role.id,surgeon_role.id)
            if self.role.id == surgeon_role.id:
                print('hi_______________________')
                result.append((0,0,{
                    'surgeon_id':self._origin.id}))
                self.allowed_surgeon_ids = result
        else:
            self.allowed_surgeon_ids.unlink()

    # original method

    # @api.onchange('boolean_check')
    # def set_domain_for_customer_type_field(self) :
    #     result = {}
    #     customer_type_id = self.env['customer.type'].search(
    #         ['|', ('name', '=ilike', 'Patient'), ('name', '=ilike', 'Doctor')])
    #     customer_type_ids = [i.id for i in customer_type_id]
    #     customer_req_type_id = self.env['customer.type'].search([])
    #     data = [j.id for j in customer_req_type_id]
    #     print('data_____list____________',data)
    #     for k in customer_type_ids:
    #         print('k______________',k)
    #         while (data.count(k)) :
    #             data.remove(k)
    #     print('data_________________',data)
    #     result['domain'] = {'customer_type' : [('id', 'in', data)]}
    #     print('result______________',result)
    #     return result

    @api.onchange('boolean_check')
    def set_domain_for_customer_type_field(self) :
        result = {}
        patient_doctor_ids = self.env['customer.type'].search(
            ['|', ('name', '=ilike', 'Patient'), ('name', '=ilike', 'Doctor')]).ids
        customer_type_ids = self.env['customer.type'].search([]).ids
        customer_required_type_ids = [x for x in customer_type_ids if x not in patient_doctor_ids]
        result['domain'] = {'customer_type' : [('id', 'in', customer_required_type_ids)]}
        return result

    def default_get(self, fields):
        if 'customer_key' in self._context:
            print('self_________________',self._context)
            if self.boolean_check == False:
                self.write({'boolean_check':True})
            if self.boolean_check == True:
                self.write({'boolean_check':False})
            self.set_domain_for_customer_type_field()
        res = super(ResPartner, self).default_get(fields)
        return res


