# -*- coding: utf-8 -*-


from odoo import api, fields, models, _ 
from odoo.exceptions import UserError

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    seq_no = fields.Char(string="Service Number", readonly=True, required=True, copy=False, default='New',tracking=True)
    degree = fields.Many2many('degree.data', 'nurse_degree_table_rel', 'nurse_id', 'degree_id', string='Qualifications',tracking=True)
    institute = fields.Char('Graduation Institute',tracking=True)
    role = fields.Many2many('role.data', 'nurse_role_table_rel', 'nurse_id', domain=[('type', '=', 'nurse')],
                            string='Roles',tracking=True)
    nmc_no = fields.Char('NMC Nr',tracking=True)
    # work_mobile = fields.Char('Work Mobile')
    work_email = fields.Char('Work Email',tracking=True)
    city = fields.Char(string="City",tracking=True)
    street = fields.Char("Street",tracking=True)
    street2 = fields.Char("Street2",tracking=True)
    nurse_zip = fields.Char("Zip",tracking=True)
    state_id = fields.Many2one('res.country.state', string="Status",tracking=True)
    nurse_country_id = fields.Many2one('res.country', string="Country",tracking=True)
    # health_centre_id = fields.Many2one("health.center", 'Surgical Centre')
    health_centre_id = fields.Many2many("health.center",'nurse_health_center_table_rel','nurse_id','center_id','Surgical Centre',tracking=True)
    # citizenship = fields.Char('Citizenship')
    citizenship_ids = fields.Many2many('res.country','nurse_id_country_id_relation','nurse_id','country_id',string='Citizenship',tracking=True)
    nurse_permit_attach_ids = fields.Many2many("ir.attachment", "nurse_id_ir_attachment_relation", 
        "nurse_id", "attachment_id", string="Attachments",tracking=True)
    national_insurance_no = fields.Char('NI Nr',tracking=True)
    work_permit = fields.Selection([('yes', 'Yes'), ('no', 'No')],tracking=True)
    work_validity = fields.Date('Work Permit Validity',tracking=True)
    dbs_no = fields.Char('DBS Nr',tracking=True)
    certification_validity = fields.Date('Validity',tracking=True)
    is_nurse = fields.Boolean('Is Nurse',tracking=True)
    availibility_check = fields.Boolean('Availibility Check',copy=False,tracking=True)
    nurse_dob = fields.Date(string="DOB",tracking=True)
    nurse_general_info_ids = fields.Many2many("ir.attachment", "employee_id_ir_attachment_relation", 
        "employee_id", "attachment_id", string="Attachments",tracking=True)
    vaccine_ids = fields.One2many('nurse.vaccination','nurse_employee_id',string='Vaccination',tracking=True)
    training = fields.Char(string="Training",tracking=True)
    bank_name = fields.Char('Bank Name',tracking=True)
    acc_no = fields.Char('Account Nr', size=8, help='Enter 8 Digit Account Number',tracking=True)
    swift_code = fields.Char('Swift Code',tracking=True)
    iban_code = fields.Char('IBAN Code',tracking=True)
    sort_code = fields.Char('Sort Code', size=6, help='Enter 6 Digit Sort Code',tracking=True)
    # title_nurse = fields.Many2one('title.name',string='Title',tracking=True)
    nurse_sex = fields.Selection([('male','Male'),('female','Female'),('other','Other')],string='Sex',tracking=True)



    @api.model
    def create(self, vals):
        if vals.get('is_nurse') == True:
            if vals.get('seq_no', 'New') == 'New':
                vals['seq_no'] = self.env['ir.sequence'].next_by_code(
                    'hr.employee') or 'New'
        result = super(HrEmployee, self).create(vals)
        print('self____________', self,result)
        return result

    @api.onchange('nurse_country_id')
    def _onchange_nurse_country_id(self) :
        if self.nurse_country_id and self.nurse_country_id != self.state_id.country_id :
            self.state_id = False

    @api.onchange('state_id')
    def _onchange_state(self) :
        if self.state_id.country_id :
            self.nurse_country_id = self.state_id.country_id



class NurseVaccine(models.Model):
    _name = "nurse.vaccination"
    _description = "Nurse Vaccination Record"

    name = fields.Char('Vaccine',tracking=True)
    date = fields.Date('Vacccination Date',tracking=True)
    validity_date = fields.Date('Validity',tracking=True)
    nurse_employee_id = fields.Many2one('hr.employee',string='Nurse',tracking=True)
    certificate_ids = fields.Many2many("ir.attachment", "nurse_employee_id_ir_attachment_relation", 
        "nurse_employee_id", "attachment_id", string="Certificate",tracking=True)
