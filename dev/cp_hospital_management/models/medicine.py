# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Medicine(models.Model):
    _name='medicine'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Medicine"

    name=fields.Char('Medicine Name',required=True)
    medicament_type=fields.Selection([('Medicine','Medicine'),('Vaccine','Vaccine')],'Medicament Type')
    therapeutic_action=fields.Char()
    qty_available=fields.Float('Stock',readonly=True)
    lst_price=fields.Float('Price')
    pregnancy_warning=fields.Boolean()

    pregnancy=fields.Text('Pregnancy and Lactancy')
    composition=fields.Text()
    dosage=fields.Text()
    adverse_reaction=fields.Text()
    indications=fields.Text()
    overdosage=fields.Text()
    storage=fields.Text()
    info=fields.Text()

    @api.model
    def create(self, vals):

        name = self.search([('name', '=', vals['name'])])
        if name:
            raise UserError(_("Medicine Already Exist."))

        category_id = self.env['product.category'].search([('name', '=', 'Medicine')]).id

        self.env['product.product'].create({
            'name': vals['name'],
            'type': 'consu',
            'categ_id':category_id,
            'list_price': vals.get('lst_price', 0.0),
            })
        return super(Medicine, self).create(vals)


    # @api.multi
    def write(self, vals):
        if vals:
            if vals.get('name'):
                name = self.search([('name', '=', vals['name'])])
                if name:
                    raise UserError(_("Medicine Already Exist."))

            product = self.env['product.product'].search([('name', '=', self.name)])
            if not product:
                raise UserError(_("This medicine is no more exist in product."))
            if vals.get('name'):
                product.name=vals['name']
            if vals.get('lst_price'):
                product.list_price=vals['lst_price']

        return super(Medicine, self).write(vals)

    # @api.multi
    def unlink(self):
        self.env['product.product'].search([('name', '=', self.name)]).unlink()
        return super(Medicine, self).unlink()

