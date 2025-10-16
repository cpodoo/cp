from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    rent_before_delivery_reminder_days = fields.Integer(
        string="Delivery Reminder Days",
    )
