from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    period = fields.Integer(
        "Warranty Expire Notification", store=True, default=1)

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    period = fields.Integer(
        "Warranty Expire Notification", related="company_id.period", readonly=False
    )
    # extract_in_invoice_digitalization_mode = fields.Selection([
    #     ('manual', 'Manual'),
    #     ('auto', 'Automatic')
    # ], string="Extract in Invoice Digitalization Mode")
