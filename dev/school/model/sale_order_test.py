from odoo import models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def send_mail(self):
        template = self.env.ref('school.mail_template_sale_order')
        if template:
            template.send_mail(self.id, force_send=True)
        else:
            raise UserError("Mail Template not found.")
