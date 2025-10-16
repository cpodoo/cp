# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = "res.partner"

    doc_seq_no = fields.Char(string="Doctor Service Number", readonly=True, copy=False, default='New',tracking=True)
    is_doctor = fields.Boolean('Is Doctor',tracking=True)
    speciality = fields.Many2one('speciality.data', string='Speciality',tracking=True)
    role = fields.Many2one('role.data', domain=[('type', '=', 'doc')], string='Roles',tracking=True)
    degree = fields.Many2many('degree.data', 'doc_degree_table_rel', 'doc_id', string='Qualifications',tracking=True)
    grad = fields.Char('Graduation Institute',tracking=True)
    gmc_no = fields.Char('GMC Nr',tracking=True)
    mobile = fields.Char('Work Mobile',tracking=True)
    email = fields.Char('Work Email',tracking=True)
    secretary_name = fields.Char('Secretary Name',tracking=True)
    secretary_phn = fields.Char('Secretary Phone Nr',tracking=True)
    secretary_tel = fields.Char('Secretary Mobile Nr',tracking=True)
    secretary_email = fields.Char('Secretary Email Id',tracking=True)
    note = fields.Text('Other Remarks',tracking=True)
    health_centre_id = fields.Many2many("health.center",'doc_health_center_table_rel','doctor_id','center_id','Surgical Centre',tracking=True)
    doc_dob = fields.Date('DOB',tracking=True)
    general_info_attach = fields.Many2many('ir.attachment','general_info_attach_rel','doc_id','attach_info_id',string="Attachments",tracking=True)
    bank_name = fields.Char('Bank Name',tracking=True)
    acc_no = fields.Char('Account Nr', size=8, help='Enter 8 Digit Account Number',tracking=True)
    swift_code = fields.Char('Swift Code',tracking=True)
    iban_code = fields.Char('IBAN Code',tracking=True)
    sort_code = fields.Char('Sort Code', size=6, help='Enter 6 Digit Sort Code',tracking=True)
    insurance_name = fields.Char('Insurance Name',tracking=True)
    policy_no = fields.Char('Policy Nr',tracking=True)
    start_date = fields.Date('Start Date',tracking=True)
    end_date = fields.Date('End Date',tracking=True)
    insurance_provider = fields.Char('Insurance Provider',tracking=True)
    insurance_attach = fields.Many2many('ir.attachment', string="Attachments",tracking=True)
    citizenship = fields.Many2many('res.country','country_attach_rel','doctor_id','citizenship_id',string='Citizenship',tracking=True)
    national_insurance_no = fields.Char('NI Nr',tracking=True)
    work_permit = fields.Selection([('yes', 'Yes'), ('no', 'No')],tracking=True)
    work_validity = fields.Date('Work Permit Validity',tracking=True)
    permit_attach = fields.Many2many("ir.attachment", "partner_id_ir_attachment_relation", "partner_id", "attachment_id", string="Attachments",tracking=True)
    country_id_loc = fields.Many2one('res.country', string="Country",tracking=True)
    city_loc = fields.Char(string="City",tracking=True)
    street_loc = fields.Char("Street",tracking=True)
    street2_loc = fields.Char("Street2",tracking=True)
    zip_loc = fields.Char("Zip",tracking=True)
    state_id_loc = fields.Many2one('res.country.state', string="Status",tracking=True)
    country_id = fields.Many2one('res.country', string="Country",tracking=True)
    city = fields.Char(string="City",tracking=True)
    street = fields.Char("Street",tracking=True)
    street2 = fields.Char("Street2",tracking=True)
    doc_zip = fields.Char("Zip",tracking=True)
    state_id = fields.Many2one('res.country.state', string="Status",tracking=True)
    procedure_ids = fields.One2many('doctor.procedures','doctor_id',string='Procedures',tracking=True)
    membership_ids = fields.One2many('doctor.membership','doctor_id',string='Affiliation and Membership',tracking=True)
    practising_privileges_attach = fields.Many2many('ir.attachment','practising_privileges_attach_attach_rel','doc_id','attach_id',string="Attachment",tracking=True)
    availibility_check = fields.Boolean('Availibility Check',copy=False,tracking=True)
    doc_sex = fields.Selection([('male','Male'),('female','Female'),('other','Other')],string='Sex',tracking=True)
    vaccine_ids = fields.One2many('vaccination','doctor_id',string='Vaccination',tracking=True)
    training = fields.Char('Training',tracking=True)

    @api.onchange('country_id_loc')
    def _onchange_country_id_loc(self):
        if self.country_id_loc and self.country_id_loc != self.state_id_loc.country_id:
            self.state_id_loc = False

    @api.onchange('state_id_loc')
    def _onchange_state_loc(self):
        if self.state_id_loc.country_id:
            self.country_id_loc = self.state_id_loc.country_id

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ResPartner, self).create(vals_list)
        if len(str(res.acc_no)) > 8:
            raise UserError('Account number should not be more than 8 digit')
        if len(str(res.sort_code)) > 6:
            raise UserError('Sort code should not be more than 6 digit')
        if res.start_date and res.end_date:
            if res.start_date > res.end_date:
                raise UserError('Insurance start date should be set before end date')
        return res

    # def write(self, vals):
    #     res = super(ResPartner, self).write(vals)
    #     if len(str(self.acc_no)) > 8:
    #         raise UserError('Account Number Should not be more than 8 digit')
    #     if len(str(self.sort_code)) > 6:
    #         raise UserError('Sort Code Should not be more than 6 digit')
    #     if self.start_date and self.end_date:
    #         if self.start_date > self.end_date:
    #             raise UserError('Insurance start date should be set before end date')
    #     return res

    def write(self, vals):
        # --- Perform checks BEFORE calling super, looping through each record ---
        for record in self:
            # Check account number length - consider the value being written OR the existing value
            acc_no_to_check = vals.get('acc_no', record.acc_no) # Get potential new value first
            if acc_no_to_check and len(str(acc_no_to_check)) > 8:
                # Add partner name to error for clarity
                raise UserError(_("Account Number Should not be more than 8 digits for partner %s") % record.display_name)

            # Check sort code length - consider the value being written OR the existing value
            sort_code_to_check = vals.get('sort_code', record.sort_code)
            if sort_code_to_check and len(str(sort_code_to_check)) > 6:
                 raise UserError(_("Sort Code Should not be more than 6 digits for partner %s") % record.display_name)

            # Check insurance dates - consider values being written OR existing values
            # Get the start/end date either from the vals being written or the current record
            start_date = vals.get('start_date', record.start_date)
            end_date = vals.get('end_date', record.end_date)

            # Ensure dates are compared correctly (need date objects if they are strings)
            if start_date and end_date:
                # Convert to date objects if they are not already (depends on how vals provides them)
                # This might not be necessary if vals already contains date objects
                start_date_obj = fields.Date.to_date(start_date) if isinstance(start_date, str) else start_date
                end_date_obj = fields.Date.to_date(end_date) if isinstance(end_date, str) else end_date

                if start_date_obj > end_date_obj:
                    raise UserError(_("Insurance start date should be set before end date for partner %s") % record.display_name)

        # --- Call super AFTER the loop and checks ---
        res = super(ResPartner, self).write(vals)
        # Add any logic needed AFTER the write completes here
        return res

    def default_get(self, fields):
        if 'doctor' in self._context:
            self.is_doctor = True
            doctor_id = self.env['customer.type'].search([('name', '=ilike', 'Doctor')])
            self.write({'customer_type':doctor_id.id})
        res = super(ResPartner, self).default_get(fields)
        return res

class Vaccine(models.Model):
    _name = "vaccination"
    _description = "Doctor Vaccination Record"

    name = fields.Char('Vaccine',tracking=True)
    date = fields.Date('Vacccination Date',tracking=True)
    validity_date = fields.Date('Validity',tracking=True)
    doctor_id = fields.Many2one('res.partner',string='Doctor',tracking=True)
    certificate_ids = fields.Many2many("ir.attachment", "vaccination_id_ir_attachment_relation", 
        "vaccination_id", "attachment_id", string="Certificate",tracking=True)