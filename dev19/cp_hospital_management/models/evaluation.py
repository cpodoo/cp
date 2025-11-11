# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date

class Evaluation(models.Model):
    _name = 'evaluation'
    _description = "Evaluation"
    _inherit = ['mail.thread', 'mail.activity.mixin']  

    name = fields.Char(string='Evaluation', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    patient = fields.Many2one('res.partner', string='Patient', required=True)
    doctor = fields.Many2one('hr.employee', string='Physician', required=True)    
    evaluation_type = fields.Selection([
        ('Ambulatory', 'Ambulatory'),
        ('Emergency', 'Emergency'),
        ('Inpatient Admission', 'Inpatient Admission'),
        ('Pre-arranged Appointment', 'Pre-arranged Appointment'),
        ('Periodic Control', 'Periodic Control'),
        ('Phonecall', 'Phonecall'),
    ], string='Evaluation Type', default='Ambulatory', required=True)
    appointment = fields.Many2one('appointment', string='Appointment')
    evaluation_start_date = fields.Date('Evaluation Start Date', default=lambda self: date.today(), required=True)
    evaluation_end_date = fields.Date(string='Evaluation End Date')
    chief_complaint = fields.Char(string='Chief Complaint')
    notes_complaint = fields.Text(string='Complaint Notes')

    temperature = fields.Float(string='Temperature (°C)')
    diastolic = fields.Float(string='Diastolic Pressure')
    respiratory_rate = fields.Float(string='Respiratory Rate')
    systolic = fields.Float(string='Systolic Pressure')
    bpm = fields.Integer(string='Heart Rate')
    osat = fields.Integer(string='Oxygen Saturation')

    weight = fields.Float(string='Weight (kg)')
    height = fields.Float(string='Height (cm)')
    abdominal_circ = fields.Float(string='Abdominal Circumference')
    head_circumference = fields.Float(string='Head Circumference')
    bmi = fields.Float(string='Body Mass Index (BMI)', readonly=True)

    edema = fields.Boolean()
    petechiae = fields.Boolean()
    acropachy = fields.Boolean()
    miosis = fields.Boolean()
    cough = fields.Boolean()
    arritmia = fields.Boolean()
    heart_extra_sounds = fields.Boolean()
    ascites = fields.Boolean()
    bronchophony = fields.Boolean()
    cyanosis = fields.Boolean()
    hematoma = fields.Boolean()
    nystagmus = fields.Boolean()
    mydriasis = fields.Boolean()
    palpebral_ptosis = fields.Boolean()
    heart_murmurs = fields.Boolean()
    jugular_engorgement = fields.Boolean()
    lung_adventitious_sounds = fields.Boolean()
    jaundice = fields.Boolean()
    hypotonia = fields.Boolean()
    masses = fields.Boolean()
    goiter = fields.Boolean()
    xerosis = fields.Boolean()
    hypertonia = fields.Boolean()

    malnutrition = fields.Boolean()
    dehydration = fields.Boolean()
    glycemia = fields.Float()
    hba1c = fields.Float(string='Glycated Hemoglobin')
    cholesterol_total = fields.Float(string='Last Cholesterol')
    ldl = fields.Float(string='Last LDL')
    hdl = fields.Float(string='Last HDL')
    tag = fields.Float(string='Last TAGs')

    pain = fields.Boolean()
    arthralgia = fields.Boolean()
    abdominal_pain = fields.Boolean()
    thoracic_pain = fields.Boolean()
    pelvic_pain = fields.Boolean()
    hoarseness = fields.Boolean()
    sore_throat = fields.Boolean()
    ear_discharge = fields.Boolean()
    chest_pain_excercise = fields.Boolean()
    astenia = fields.Boolean()
    weight_change = fields.Boolean()
    hemoptysis = fields.Boolean()
    epistaxis = fields.Boolean()
    rinorrhea = fields.Boolean()
    vomiting = fields.Boolean()
    polydipsia = fields.Boolean()
    polyuria = fields.Boolean()
    vesical_tenesmus = fields.Boolean()
    dysuria = fields.Boolean()

    pain_intensity = fields.Integer(help='Pain Intensity from 0 (no pain) to 10 (worst possible pain).')
    myalgia = fields.Boolean()
    cervical_pain = fields.Boolean()
    lumbar_pain = fields.Boolean()
    headache = fields.Boolean()
    odynophagia = fields.Boolean()
    otalgia = fields.Boolean()
    chest_pain = fields.Boolean()
    orthostatic_hypotension = fields.Boolean()
    anorexia = fields.Boolean()
    abdominal_distension = fields.Boolean()
    hematemesis = fields.Boolean()
    gingival_bleeding = fields.Boolean()
    nausea = fields.Boolean()
    dysphagia = fields.Boolean()
    polyphagia = fields.Boolean()
    nocturia = fields.Boolean()
    pollakiuria = fields.Boolean()

    mood_swings = fields.Boolean()
    pruritus = fields.Boolean()
    disturb_sleep = fields.Boolean()
    orthopnea = fields.Boolean()
    paresthesia = fields.Boolean()
    dizziness = fields.Boolean()
    tinnitus = fields.Boolean()
    eye_glasses = fields.Boolean()
    diplopia = fields.Boolean()
    dysmenorrhea = fields.Boolean()
    metrorrhagia = fields.Boolean()
    vaginal_discharge = fields.Boolean()
    diarrhea = fields.Boolean()
    rectal_tenesmus = fields.Boolean()
    proctorrhagia = fields.Boolean()
    sexual_dysfunction = fields.Boolean()
    stress = fields.Boolean()
    insomnia = fields.Boolean()
    dyspnea = fields.Boolean()
    amnesia = fields.Boolean()
    paralysis = fields.Boolean()
    vertigo = fields.Boolean()
    syncope = fields.Boolean()
    blurry_vision = fields.Boolean()
    photophobia = fields.Boolean()
    amenorrhea = fields.Boolean()
    menorrhagia = fields.Boolean()
    urethral_discharge = fields.Boolean()
    constipation = fields.Boolean()
    melena = fields.Boolean()
    xerostomia = fields.Boolean()

    loc = fields.Integer(string='Level of Consciousness')
    loc_verbal = fields.Integer(string='Level of Consciousness - Verbal')
    loc_eyes = fields.Integer(string='Level of Consciousness - Eyes')
    loc_motor = fields.Integer(string='Level of Consciousness - Motor')

    mood = fields.Selection([
        ('Normal', 'Normal'),
        ('Sad', 'Sad'),
        ('Fear', 'Fear'),
        ('Rage', 'Rage'),
        ('Happy', 'Happy'),
        ('Disgust', 'Disgust')
    ], string="Mood")
    orientation = fields.Boolean()
    knowledge_current_events = fields.Boolean(string='Knowledge of Current Events')
    abstraction = fields.Boolean()
    calculation_ability = fields.Boolean()
    praxis = fields.Boolean()
    violent_behaviour = fields.Boolean()
    memory = fields.Boolean()
    judgement = fields.Boolean()
    vocabulary = fields.Boolean()
    object_recognition = fields.Boolean()

    info_diagnosis = fields.Text(string="Diagnosis Info")
    directions = fields.Text(string="Directions")
    notes = fields.Text()

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('evaluation') or '/'
        return super(Evaluation, self).create(vals)

    def default_get(self, fields):
        res = super().default_get(fields)
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        if employee:
            res['doctor'] = employee.id
        return res

    @api.onchange('weight', 'height')
    def onchange_weight_height(self):
        if self.weight and self.height:
            try:
                self.bmi = self.weight / ((self.height / 100) ** 2)
            except ZeroDivisionError:
                self.bmi = 0
        else:
            self.bmi = 0
