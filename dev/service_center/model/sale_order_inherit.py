from odoo import api,models
from odoo.exceptions import ValidationError

class SaleOrderLineInherit(models.Model):
    _inherit='sale.order.line'

    @api.model
    def write(self,vals):
        result =super(SaleOrderLineInherit,self).write(vals)
        if self.discount:
            print(self.discount)
            if self.discount > 30 or self.discount < 0:
                raise ValidationError("Greater than 30% discount is not allow")
        return result
