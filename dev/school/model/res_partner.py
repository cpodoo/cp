from odoo import api, models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_copy_phone_to_mobile(self):
        for record in self:
            if record.phone and not record.mobile:
                record.write({'mobile' : record.phone})

    class ResPartner(models.Model):
        _inherit = "res.partner"
        vehicle_count = fields.Integer(string="Vehicles",
                                       compute='compute_vehicle_count',
                                       default=0)

        def compute_vehicle_count(self):
            for record in self:
                record.vehicle_count = self.env['fleet.vehicle'].search_count(
                    [('driver_id', '=', self.id)])



    # preferred_contact_method = fields.Selection([
    #     ('email', 'Email'),
    #     ('phone', 'Phone'),
    #     ('postal', 'Postal Mail'),
    # ], string='Preferred Contact Method')
    #
    # @api.model
    # def create(self, vals):
    #     # Custom logic
    #     if 'preferred_contact_method' not in vals:
    #         vals['preferred_contact_method'] = 'email'  # Set default value
    #     return super(ResPartner, self).create(vals)
