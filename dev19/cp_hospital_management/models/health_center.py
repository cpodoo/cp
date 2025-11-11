# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HealthCenter(models.Model):
    _name="health.center"
    _description = "Health Center"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    image = fields.Binary(attachment=True)
    name=fields.Char("Hospital Name", required=True)
    health_center_type=fields.Selection([('hospital','Hospital'),('nursing','Nursing Home'),('clinic','Clinic'),('community','Community Health Center'),('other','Other')], string="Health Center Type", required=True)
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    email = fields.Char()
    phone = fields.Char()
    fax = fields.Char()
    mobile = fields.Char()
    website = fields.Char(help="Website of Partner or Company")
    info=fields.Text()


class HealthCenterBuilding(models.Model):
    _name="health.center.building"
    _description = "Health Center Building"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name=fields.Char("Building Name", required=True)
    institution=fields.Many2one('health.center',string='Health Center',required=True)
    code=fields.Char(size=64)
    info=fields.Text()


class HealthCenterWard(models.Model):
    _name="health.center.ward"
    _description = "Health Center Ward"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    name=fields.Char("Ward Name", required=True)
    state = fields.Selection(
        [('Beds Available', 'Beds Available'), ('Full', 'Full')], 'State', default='Beds Available')
    institution=fields.Many2one('health.center','Health Center',required=True)
    building = fields.Many2one('health.center.building', required=True)
    floor=fields.Integer('Floor Number')
    private=fields.Boolean('Private Room')
    gender=fields.Selection([('men','Men Ward'),('women','Women Ward'),('unisex','Unisex')], 'Type')
    bio_hazard=fields.Boolean('Bio Hazard')
    telephone=fields.Boolean('Telephone Access')
    private_bathroom=fields.Boolean()
    tv=fields.Boolean('Television')
    refrigerator=fields.Boolean()
    ac=fields.Boolean('Air Conditioning')
    guest_sofa=fields.Boolean('Guest Sofa')
    internet=fields.Boolean('Internet Access')
    microwave=fields.Boolean('')
    info=fields.Text()

class HealthCenterBeds(models.Model):
    _name = "health.center.beds"
    _description = "Health Center Beds"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name=fields.Char("Bed Name", required=True)
    state = fields.Selection(
        [('Free', 'Free'), ('Reserved', 'Reserved'),('Occupied','Occupied'),('Not Available','Not Available')], 'State')
    institution = fields.Many2one('health.center', 'Health Center', required=True)
    building = fields.Many2one('health.center.building', required=True)
    ward = fields.Many2one('health.center.ward', required=True)
    telephone_number=fields.Char()
    list_price=fields.Float('Reservation Charge')
    bed_type=fields.Selection([('Gatch Bed','Gatch Bed'),('Electric','Electric'),
                               ('Strecher','Strecher'),('Low Bed','Low Bed'),('Low Air Loss','Low Air Loss'),
                               ('Circo Electric','Circo Electric'),('Clinitron','Clinitron')],'Bed Type',required=True)
    change_bed_status=fields.Selection([('Free','Free'),('Mark as Reserved','Mark as Reserved'),('Mark as Occupied','Mark as Occupied'),
                                        ('Mark as Not Available','Mark as Not Available')],'Change Bed Status',default='Free',required=True)
    info=fields.Text()

    @api.onchange('change_bed_status')
    def onchange_bedstate(self):

        if self.change_bed_status == 'Free':
            self.state = 'Free'

        elif self.change_bed_status == 'Mark as Reserved':
            self.state = 'Reserved'

        elif self.change_bed_status == 'Mark as Not Available':
            self.state='Not Available'

        elif self.change_bed_status == 'Mark as Occupied':
            self.state='Occupied'

        elif self.change_bed_status == 'Mark as Not Available':
            self.state='Not Available'

class HealthCenterOt(models.Model):
    _name = "health.center.ot"
    _description = "Health Center OT"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name=fields.Char("OT Name", required=True)
    state = fields.Selection(
        [('Free', 'Free'), ('Reserved', 'Reserved'), ('Occupied', 'Occupied'), ('Not Available', 'Not Available')],
        'State', readonly=True, default='Free')
    building = fields.Many2one('health.center.building', required=True)
    institution = fields.Many2one('health.center', 'Health Center', required=True)

    info=fields.Text()

    def set_to_free(self):
        self.write({'state': 'Free'})

    def set_to_reserved(self):
        self.write({'state': 'Reserved'})

    def set_to_occupied(self):
        self.write({'state': 'Occupied'})

    def set_to_not_available(self):
        self.write({'state':'Not Available'})

class HealthCenterPharmacy(models.Model):
    _name = "health.center.pharmacy"
    _description = "Health Center Pharmacy"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    image = fields.Binary(attachment=True)
    name=fields.Char("Pharmacy Name")
    institution = fields.Many2one('health.center', 'Health Center')
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    email = fields.Char()
    phone = fields.Char()
    fax = fields.Char()
    mobile = fields.Char()
    website = fields.Char(help="Website of Partner or Company")
    info = fields.Text()

    prescription_line_ids=fields.One2many('prescription.line','pharmacy')

class HealthCenterDomiciliaryUnit(models.Model):
    _name = "health.center.domiciliary.unit"
    _description = "Health Center Domiciliary Unit"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    picture = fields.Binary(attachment=True)
    name=fields.Char(size=128)
    institution = fields.Many2one('health.center', 'Health Center')
    desc=fields.Char("Description",size=25)
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    address_city = fields.Char()
    address_state= fields.Many2one("res.country.state", string='State', ondelete='restrict')
    address_country= fields.Many2one('res.country', string='Country', ondelete='restrict')
    email = fields.Char()
    phone = fields.Char()
    fax = fields.Char()
    mobile = fields.Char()
    housing=fields.Selection([('Shanty,Deficient sanitary conditions ','Shanty,Deficient sanitary conditions '),
                              ('Small, crowded but with good sanitary conditions','Small, crowded but with good sanitary conditions'),
                              ('Comfortable and good sanitary conditions','Comfortable and good sanitary conditions'),
                              ('Roomy and excellent sanitary conditions','Roomy and excellent sanitary conditions'),
                              ('Luxury and excellent sanitary conditions','Luxury and excellent sanitary conditions')],'Conditions')
    materials=fields.Selection([('Concrete','Concrete'),('Adobe','Adobe'),('Wood','Wood'),
                                ('Mud/Straw','Mud/Straw'),('Stone','Stone')],'Material')
    bathrooms=fields.Integer()
    total_surface=fields.Integer('Surface')
    dwelling=fields.Selection([('Single/Detached House','Single/Detached House'),('Apartment','Apartment'),('Townhouse','Townhouse'),
                               ('Factory','Factory'),('Building','Building'),('Mobile House','Mobile House')],'Type')
    roof_type=fields.Selection([('Concrete','Concrete'),('Adobe','Adobe'),('Wood','Wood'),
                                ('Thatched','Thatched'),('Mud/Straw','Mud/Straw'),('Stone','Stone')],'Roof')
    bedrooms=fields.Integer()
    sewers=fields.Boolean('Sanitary Sewers')
    trash=fields.Boolean('Trash Recollection')
    gas=fields.Boolean('Gas Supply')
    television=fields.Boolean('Television')
    water=fields.Boolean('Running Water')
    electricity=fields.Boolean('Electrical Supply')
    telephone=fields.Boolean('Telephone')
    internet=fields.Boolean('Internet')