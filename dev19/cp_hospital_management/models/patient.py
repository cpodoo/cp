# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Patient(models.Model):
    _inherit = 'res.partner'

    is_patient=fields.Boolean('Is Patient')
    bdate=fields.Date("Date of Birth")
    blood_type=fields.Selection([('O','O'),('A','A'),('B','B'),('AB','AB')],string="Blood Type")
    rh=fields.Selection([('+','+'),('-','-')],string="Rh")
    sex=fields.Selection([('Male','Male'),('Female','Female')],string="Gender")
    responsible=fields.Many2one('res.users',default=lambda self: self.env.user)
    marital_status=fields.Selection([('s','Single'),('m','Married')],string="Marital Status")
    family_phy=fields.Many2one('hr.employee',"Family Physician")
    patient_deceased=fields.Boolean("Patient Deceased ?")
    socio=fields.Char("Socioeconomics")
    works_at_home=fields.Boolean()
    Edu_level=fields.Char("Education level")
    hour_out_home=fields.Float("Hours stay outside home")
    house_condition=fields.Text("Housing Condition")
    occupation=fields.Char()
    income=fields.Char("Income(Monthly)")
    sanitary_sewers=fields.Boolean()
    gas_supply=fields.Boolean()
    running_water=fields.Boolean()
    telephone=fields.Boolean()
    trash_recollection=fields.Boolean()
    television=fields.Boolean()
    elctrical_supply=fields.Boolean()
    internet=fields.Boolean()
    family_help=fields.Char()
    family_time_sharing=fields.Char()
    family_discuss=fields.Char("Family discussions on problems")
    family_affection=fields.Char()

    family=fields.One2many('patient.family','family_id')

    lab_test_ids=fields.One2many('lab.tests','patient',readonly=True)
    prescription_line=fields.One2many('prescription.line','patient',readonly=True)
    evaluation_ids=fields.One2many('evaluation','patient')
    surgery_ids=fields.One2many('surgery','patient')

    call_log_ids=fields.One2many('call.log','patient')

    exercise = fields.Boolean()
    exercise_minutes_day = fields.Integer("Minutes/Day")
    sleep_during_daytime = fields.Boolean('Sleeps at Daytime')
    sleep_hours=fields.Integer('Hours of Sleep')
    number_of_meals=fields.Integer('Meals / Day')
    eats_alone=fields.Boolean()
    coffee=fields.Boolean()
    coffee_cups=fields.Integer('Cups / Day')
    soft_drinks=fields.Boolean('Soft Drinks(sugar)')
    salt=fields.Boolean()
    diet=fields.Boolean('On Diet?')
    diet_info=fields.Char('Diet Info')
    lifestyle_info=fields.Text()

    smoking=fields.Boolean()
    ex_smoker=fields.Boolean('Ex Smoker')
    age_start_smoking=fields.Integer('Age Started Smoking')
    smoking_number=fields.Integer('Cigarretes / Day')
    passive_smoker=fields.Boolean('Passive Smoker')
    age_quit_smoking=fields.Integer('Age of Quitting')

    alcohol=fields.Boolean('Drinks Alcohol')
    age_start_drinking=fields.Integer('Age Started Drinking')
    alcohol_beer_number=fields.Integer('Beer / Day')
    alcohol_liquor_number=fields.Integer('Liquor / Day')
    ex_alcoholic=fields.Boolean('Ex Alcoholic')
    age_quit_drinking=fields.Integer('Age Quited Drinking')
    alcohol_wine_number=fields.Integer('Wine / Day')

    drug_usage=fields.Boolean('Drug Habit')
    age_start_drugs=fields.Integer('Age Started Drug')
    age_quit_drugs=fields.Integer('Age Quited Drug')
    ex_drug_addict=fields.Boolean('Ex Drug Addict')
    drug_iv=fields.Boolean('IV Drug User')

    app_count = fields.Integer(compute='_compute_appointments')
    prescription_count = fields.Integer(compute='_compute_prescriptions')
    vaccine_count = fields.Integer(compute='_compute_vaccines')
    admission_count = fields.Integer(compute='_compute_admissions')
    evaluation_count = fields.Integer(compute='_compute_evaluations')
    surgery_count = fields.Integer(compute='_compute_surgeries')
    lab_test_count = fields.Integer(compute='_compute_lab_tests')
    short_name = fields.Char('Short name')
    customer_type = fields.Many2one('customer.type',string='Customer Type',tracking=True)


    def _compute_appointments(self):
        Appointment=self.env['appointment']
        self.app_count=Appointment.search_count([('patient.id', '=', self.id)])

    def _compute_prescriptions(self):
        Prescription = self.env['prescription']
        self.prescription_count = Prescription.search_count([('patient.id', '=', self.id)])

    def _compute_vaccines(self):
        Vaccine = self.env['vaccine']
        self.vaccine_count = Vaccine.search_count([('patient.id', '=', self.id)])

    def _compute_admissions(self):
        Admission = self.env['inpatient.admissions']
        self.admission_count = Admission.search_count([('patient.id', '=', self.id)])

    def _compute_evaluations(self):
        Evaluation = self.env['evaluation']
        self.evaluation_count = Evaluation.search_count([('patient.id', '=', self.id)])

    def _compute_surgeries(self):
        Surgery = self.env['surgery']
        self.surgery_count = Surgery.search_count([('patient.id', '=', self.id),('state','=','Done')])

    def _compute_lab_tests(self):
        Lab_Tests = self.env['lab.tests']
        self.lab_test_count = Lab_Tests.search_count([('patient.id', '=', self.id)])

class PatientFamily(models.Model):
    _name='patient.family'
    _description = "Patient Family"

    family_id=fields.Many2one('res.partner')
    name=fields.Char(required=True)
    relation=fields.Selection([('Father','Father'),('Mother','Mother'),('Brother','Brother'),('Sister','Sister'),
                               ('Wife','Wife'),('Husband','Husband'),('Grand Father','Grand Father'),('Grand Mother','Grand Mother'),
                               ('Aunt','Aunt'),('Uncle','Uncle'),('Nephew','Nephew'),('Niece','Niece'),('Cousin','Cousin'),
                               ('Relative','Relative'),('Ohter','Other'),])
    age=fields.Integer()