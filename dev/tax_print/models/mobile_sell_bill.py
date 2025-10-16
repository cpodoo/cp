from odoo import models, fields, api
from odoo.exceptions import UserError

class MobileSellBill(models.Model):
    _name = 'mobile.sell.bill'
    _description = 'Mobile Sell Bill'
    # _order = 'id desc'

    name = fields.Char(string="Bill No", required=True, copy=False, readonly=True, default='New')
    date = fields.Date(string="Date", default=fields.Date.today)
    phone_model = fields.Char(string="Mobile Model")
    imei_number = fields.Char(string="IMEI Number")
    customer_name = fields.Char(string="Customer Name")
    customer_address = fields.Text(string="Customer Address")
    customer_phone = fields.Char(string="Customer Phone")
    id_proof = fields.Selection([
        ('aadhar', 'Aadhar Card'),
        ('license', 'Driving License'),
        ('voter', 'Voter Card'),
        ('pan', 'PAN Card'),
    ], string="ID Proof")
    id_proof_attachment = fields.Binary(string="Upload ID Proof")
    remarks = fields.Text(string="Remarks")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('mobile.sell.bill') or 'New'
        return super().create(vals)

    def print_sell_bill(self):
        if not self:
            raise UserError("No record selected to print.")
        return self.env.ref('tax_print.report_mobile_sell_bill_action').report_action(self)
