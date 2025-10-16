from email.policy import default

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date

class School(models.Model):
    _name = 'school.school'
    _description = "Education"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'gender'

    name = fields.Char(string="Student Name", required=True)
    _sql_constraints = [
        ('unique_student_name', 'UNIQUE(name)', 'Student name must be unique.')
    ]
    year_level = fields.Selection([('1st Year', '1st Year'), ('2nd Year', '2nd Year'), ('3rd Year', '3rd Year'),
                                   ('4th Year', '4th Year')], string="Select Year Level")
    degree = fields.Selection([('BE', 'BE'), ('B.Tech', 'B.Tech'), ('M.Tech', 'M.Tech'), ('BSC', 'BSC')],
                              string="Select Your Degree")
    email = fields.Char(string="Email")
    date = fields.Date(string="Today's Date",default=fields.Date.today)
    contact_number = fields.Char(string="Contact Number")
    date_of_birth = fields.Date(string="Date Of Birth")
    address = fields.Text(string="Address")
    high_school_name = fields.Char(string="High School Name")
    extra_curricular = fields.Selection([('student council', 'Student Council'), ('class officer', 'Class Officer'),
                                         ('club/organization', 'Club/Organization'), ('vasity player', 'Vasity Player')],
                                        string="Extra Curricular Participation")
    skills = fields.Selection([('acting', 'Acting'), ('arts/craft', 'Arts/Craft'), ('dancing', 'Dancing'),
                               ('drawing', 'Drawing')], string="Skills/Talent")
    sports = fields.Selection([('volleyball', 'Volleyball'), ('badminton', 'Badminton'), ('basketball', 'Basketball'),
                               ('swimming', 'Swimming')], string="Sports")
    parent_student_id = fields.Many2one('school.student', string="Select Student")
    image = fields.Binary(string="image")
    country = fields.Many2one('res.country', string="Country")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Select Gender")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string="Status", default='draft', tracking=True)
    referral_code = fields.Char(string="Referral Code", default="XYZ123")
    mobile = fields.Char(string="Mobile")
    planning_result = fields.Many2one('num.days', string="No.of Days")
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')

    def action_submit(self):
        for rec in self:
            rec.state = 'submitted'

    def action_approve(self):
        for rec in self:
            rec.state = 'approved'

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'

    def action_set_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    student_count = fields.Integer(
        string="Student Count",
        compute="_compute_student_count")


    def _compute_student_count(self):
        for record in self:
            record.student_count = self.env['school.school'].search_count([])

    def action_open_student(self):
         return {
                'type': 'ir.actions.act_window',
                'name': 'Student Count',
                'view_mode': 'list,form',
                'res_model': 'school.school',
                'domain': [],
                'target': 'new'}

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.email = self.name.lower().replace(' ', '')+'@school.com'

    roll_number = fields.Char(string="Roll Number", readonly=True, copy=False, default='New')

    @api.model
    def create(self, vals):
        if vals.get('roll_number', 'New') == 'New':
            vals['roll_number'] = self.env['ir.sequence'].next_by_code('student.roll.number') or 'New'
        return super(School, self).create(vals)

    # @api.model_create_multi
    # def create(self, values):
    #     # Ensure the 'mobile' field is provided
    #     if 'mobile' not in values or not values.get('mobile'):
    #         raise exceptions.ValidationError(
    #             "Mobile is a mandatory field. Please provide a mobile number.")
    #     # Call the original create method
    #     return super(School, self).create(values)

    def write(self, values):
        # Ensure the 'mobile' field is provided and not empty when updating
        if 'mobile' in values and not values['mobile']:
            raise exceptions.ValidationError(
                "Mobile is a mandatory field. Please provide a mobile number.")
        # Call the original write method to update the record
        return super(School, self).write(values)

    def send_mail(self):
        mail_template = self.env.ref('mail.mail_template_test').with_context(lang=self.env.user.lang)
        mail_template.send_mail(self.id, force_send=True)

    def action_send_welcome_email(self):
        template = self.env.ref('school.email_template_partner_basic')
        for partner in self:
            if partner.email:
                template.send_mail(partner.id, force_send=True)

    high_school_alumni_count = fields.Integer(
        string='High School Alumni',
        compute='_compute_high_school_alumni_count'
    )

    def _compute_high_school_alumni_count(self):
        for record in self:
            if record.high_school_name:
                count = self.env['school.school'].search_count([
                    ('high_school_name', '=', record.high_school_name),
                    ('id', '!=', record.id)
                ])
                record.high_school_alumni_count = count
            else:
                record.high_school_alumni_count = 0

    def action_view_high_school_alumni(self):
        self.ensure_one()
        try:
            list_view_id = self.env.ref('school.view_school_list').id
            form_view_id = self.env.ref('school.view_school_form').id
        except ValueError:
            raise UserError("Required views not found. Check XML view IDs in school_views.xml")

        return {
            'type': 'ir.actions.act_window',
            'name': _('High School Alumni'),
            'res_model': 'school.school',
            'view_mode': 'list,form',
            'views': [(list_view_id, 'list'), (form_view_id, 'form')],
            'domain': [
                ('high_school_name', '=', self.high_school_name),
                ('id', '!=', self.id)
            ],
            'context': {},
        }
    def action_get_vehicles_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vehicles',
            'view_mode': 'list',
            'res_model': 'fleet.vehicle',
            'domain': [('driver_id', '=', self.id)],
            'context': "{'create': False}"
        }

    study_duration_days = fields.Integer(string="Study Duration (Days)", compute="_compute_study_duration", store=True)

    @api.depends('start_date', 'end_date')
    def _compute_study_duration(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date >= rec.start_date:
                rec.study_duration_days = (rec.end_date - rec.start_date).days
            else:
                rec.study_duration_days = 0

    @api.onchange('start_date', 'end_date')
    def _onchange_dates(self):
        if self.start_date and self.end_date and self.end_date >= self.start_date:
            self.study_duration_days = (self.end_date - self.start_date).days
        else:
            self.study_duration_days = 0

    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': self.name + ' (Copy)',
            'roll_number': 'New',
            'study_duration_days': 0,
            'state': 'new'
        })
        return super(School, self).copy(default)

    # 1. Age from Date of Birth
    age = fields.Integer(string="Age", compute="_compute_age", store=True)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.today()
        for rec in self:
            if rec.date_of_birth:
                rec.age = (today - rec.date_of_birth).days // 365
            else:
                rec.age = 0

    # 2. Grade and Percentage
    marks_obtained = fields.Float(string="Marks Obtained")
    total_marks = fields.Float(string="Total Marks")
    percentage = fields.Float(string="Percentage", compute="_compute_percentage_and_grade", store=True)
    grade = fields.Selection([
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')
    ], string="Grade", compute="_compute_percentage_and_grade", store=True)

    @api.depends('marks_obtained', 'total_marks')
    def _compute_percentage_and_grade(self):
        for rec in self:
            if rec.total_marks:
                rec.percentage = (rec.marks_obtained / rec.total_marks) * 100
                if rec.percentage >= 90:
                    rec.grade = 'A'
                elif rec.percentage >= 75:
                    rec.grade = 'B'
                elif rec.percentage >= 60:
                    rec.grade = 'C'
                elif rec.percentage >= 40:
                    rec.grade = 'D'
                else:
                    rec.grade = 'F'
            else:
                rec.percentage = 0
                rec.grade = False

    # 3. Family Count (Same Address)
    family_count = fields.Integer(string="Family Members", compute="_compute_family_count")

    @api.depends('address')
    def _compute_family_count(self):
        for rec in self:
            if rec.address:
                rec.family_count = self.env['school.school'].search_count([
                    ('address', '=', rec.address),
                    ('id', '!=', rec.id)
                ])
            else:
                rec.family_count = 0

    student_type = fields.Selection([
        ('minor', 'Minor'),
        ('adult', 'Adult')
    ], string="Student Type", compute="_compute_student_type", store=True)

    @api.depends('age')
    def _compute_student_type(self):
        for rec in self:
            if rec.age >= 18:
                rec.student_type = 'adult'
            elif rec.age > 0:
                rec.student_type = 'minor'
            else:
                rec.student_type = False

class Student(models.Model):
    _name = 'school.student'
    _description = 'students'

    name = fields.Char(string="Student Name", required=True)

class NumDays(models.Model):
     _name = 'num.days'
     _description = 'No. of days'

     name = fields.Char(string='No. of days')

     @api.model
     def create(self, vals):
        if not vals.get('parent_student_id'):
            vals['parent_student_id'] = self.env['ir.sequence'].next_by_code('school_code')
        return super(School, self).create(vals)

     # @api.model
     # def unlink(self):
     #    for record in self:
     #        if record.name:
     #            raise UserError(_('You cannot Delete this record'))
     #        return super(School, self).unlink()
