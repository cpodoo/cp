from odoo import models, fields


class PreOpAssesment(models.Model):
    _name = "preop.assesment"
    _description = "Surgery Pre-Op Assesment"

    name = fields.Char(default='Pre-Op Assesment',tracking=True)
    date = fields.Date(string='Date',tracking=True)
    surgical_center = fields.Many2one('health.center', string='Surgical Center',tracking=True)
    procedure_date = fields.Date(string='Date of Procedure',tracking=True)
    admission_date = fields.Date(string='Admission Date',tracking=True)
    procedure_id = fields.Many2one('procedure', string='Procedure',tracking=True)
    surgeon = fields.Many2one('res.partner', string='Surgeon',tracking=True)
    anaesthesia = fields.Selection(
        [('general', 'General/TIVA'),
         ('local', 'Local')],
        string='Anaesthesia',tracking=True)
    stay = fields.Selection(
        [('day', 'Day Case'),
         ('night', 'Overnight')],
        string='Stay',tracking=True)
    id_check_by = fields.Many2one('hr.employee', string='ID Checked By', domain="[('is_nurse','=',True)]",tracking=True)

    # PATIENT INFORMATION
    # title = fields.Selection(
    #     [('mr', 'Mr.'),
    #      ('mrs', 'Mrs.'),
    #      ('ms', 'Ms.')],
    #     string='Title',tracking=True)
    height = fields.Char(string='Height',tracking=True)
    occupation = fields.Char(string='Occupation',tracking=True)
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True,tracking=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='Status', ondelete='restrict',tracking=True)
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict',tracking=True)
    home_telephone = fields.Char(string='Home Telephone',tracking=True)
    email = fields.Char(string='Email',tracking=True)

    # GP DETAILS
    nhs_number = fields.Char(string='NHS Number',tracking=True)
    gp_name = fields.Char(string='GP Name',tracking=True)
    gp_street = fields.Char()
    gp_street2 = fields.Char()
    gp_zip = fields.Char(change_default=True,tracking=True)
    gp_city = fields.Char()
    gp_state_id = fields.Many2one("res.country.state", string='Status', ondelete='restrict',tracking=True)
    gp_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict',tracking=True)
    gp_telephone = fields.Char(string='GP Telephone',tracking=True)
    gp_email = fields.Char(string='GP Email',tracking=True)

    # ADDITIONAL INFORMATION
    add_name = fields.Char(string='Name',tracking=True)
    add_street = fields.Char()
    add_street2 = fields.Char()
    add_zip = fields.Char(change_default=True,tracking=True)
    add_city = fields.Char()
    add_state_id = fields.Many2one("res.country.state", string='Status', ondelete='restrict',tracking=True)
    add_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict',tracking=True)
    add_telephone = fields.Char(string='Telephone',tracking=True)
    add_email = fields.Char(string='Email',tracking=True)
    # 29 signature

    # PATIENT’S HEALTH QUESTIONNAIRE
    chest_angina = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Chest Pain, Angina',tracking=True)
    chest_angina_text = fields.Text()
    heart_attack = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Heart Attack',tracking=True)
    heart_attack_text = fields.Text()
    palpi_heartmurmur = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='PALPITATIONS, HEART MURMUR',tracking=True)
    palpi_heartmurmur_text = fields.Text()
    high_blood_pressure = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='HIGH BLOOD PRESSURE',tracking=True)
    high_blood_pressure_text = fields.Text()
    blackout_faints = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='BLACKOUTS, FAINTS',tracking=True)
    blackout_faints_text = fields.Date()
    epilepsy_fits = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='EPILEPSY, FITS',tracking=True)
    epilepsy_fits_text = fields.Date()
    multiple_sclerosis = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='MULTIPLE SCLEROSIS',tracking=True)
    multiple_sclerosis_text = fields.Text()
    stroke_mini = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='STROKE, MINI STROKE',tracking=True)
    stroke_mini_text = fields.Text()
    bleeding_bruising = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='EXCESSIVE BLEEDING OR BRUISING',tracking=True)
    bleeding_bruising_text = fields.Text()
    anaemia = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='ANAEMIA (Excluding Pregnancy)',tracking=True)
    anaemia_text = fields.Text()
    asthma_bronchitis = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='ASTHMA, BRONCHITIS?',tracking=True)
    asthma_bronchitis_field1 = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                string='Have you had any hospital admissions with asthma in the last 6 months?',tracking=True)
    asthma_bronchitis_field2 = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                string='Have you been prescribed steroid tablets within the last 3 months related to asthma? What does?',tracking=True)
    asthma_bronchitis_field2_text = fields.Text()
    tuberclosis = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='TUBERCULOSIS',tracking=True)
    tuberclosis_text = fields.Text()
    indigestion_heartburn = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='INDIGESTION, HEART BURN',tracking=True)
    indigestion_heartburn_text = fields.Text()
    jaundice_liver = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='JAUNDICE, LIVER DISEASE (Hepatitis)',tracking=True)
    jaundice_liver_text = fields.Text()
    bowels = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='PROBLEMS WITH BOWELS',tracking=True)
    bowels_text = fields.Text()
    kidney_urinary = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='KIDNEY, URINARY PROBLEMS',tracking=True)
    kidney_urinary_text = fields.Text()
    diabetes = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='DIABETES',tracking=True)
    diabetes_text = fields.Text()
    arthritis_joint_rheumatoid = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                  string='ARTHRITIS, JOINT PROBLEMS, RHEUMATOID',tracking=True)
    arthritis_joint_rheumatoid_text = fields.Text()
    thyroid_problems = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='THYROID PROBLEMS',tracking=True)
    thyroid_problems_text = fields.Text()
    blood_clotting = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='BLOOD CLOTTING',tracking=True)
    blood_clotting_text = fields.Text()
    blood_clotting_attach = fields.Many2many('ir.attachment', relation="preopblood_attach_rel", column1="preopblood_id",tracking=True)
    sickle_cell_anaemia = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='SICKLE CELL ANAEMIA',tracking=True)
    sickle_cell_anaemia_text = fields.Text()
    sickle_cell_anaemia_attach = fields.Many2many('ir.attachment', relation="preopsickle_attach_rel",
                                                  column1="preopsickle_id",tracking=True)
    skin_problem_eczema = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='SKIN PROBLEMS, INCLUDING ECZEMA',tracking=True)
    skin_problem_eczema_char = fields.Char()
    sight_impairment = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='SIGHT IMPAIRMENT',tracking=True)
    sight_impairment_text = fields.Text()
    hearing_impairment = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='HEARING IMPAIRMENT',tracking=True)
    hearing_impairment_text = fields.Text()
    any_serious_illness = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='ANY SERIOUS ILLNESS?',tracking=True)
    any_serious_illness_text = fields.Text()
    any_operation = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='HAD ANY OPERATION?',tracking=True)
    any_operation_text = fields.Text()
    reaction_local_anaesthetic = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                  string='REACTION TO A LOCAL OR GENERAL ANAESTHETIC',tracking=True)
    reaction_local_anaesthetic_text = fields.Text()
    serious_post_ope_complication = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                     string='SERIOUS POST OPERATIVE COMPLICATIONS',tracking=True)
    serious_post_ope_complication_text = fields.Text()
    blood_transfusion = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='BLOOD TRANSFUSION ',tracking=True)
    blood_transfusion_text = fields.Text()
    blood_products = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                      string='ARE THERE ANY REASONS WHY YOU WOULD NOT ACCEPT BLOOD OR BLOOD PRODUCTS?',tracking=True)
    blood_products_text = fields.Text()
    smoker_6month_past = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='SMOKER IN THE PAST 6 MONTHS?',tracking=True)
    smoker_6month_past_text = fields.Text()
    drink_alcohol = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='DRINK ALCOHOL',tracking=True)
    drink_alcohol_text = fields.Text()
    drug_use = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='DRUG USE?',tracking=True)
    drug_use_text = fields.Text()
    drug_use_name = fields.Many2one('drug', string='Drug name',tracking=True)
    pregnant = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='PREGNANT',tracking=True)
    pregnant_text = fields.Text()
    breast_fed_3month = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='BREAST-FED IN THE LAST 3 MONTHS',tracking=True)
    breast_fed_3month_text = fields.Text()
    flight_of_stairs_without_breath = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                       string='CAN YOU CLIMB A FLIGHT OF STAIRS WITHOUT GETTING OUT OF BREATH?',tracking=True)
    flight_of_stairs_without_breath_text = fields.Text()
    anxieties_worries_concern = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                 string='PSYCHOLOGICAL ANXIETIES, WORRIES, CONCERNS',tracking=True)
    anxieties_worries_concern_text = fields.Text()
    dysmorphia = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                  string='HAVE YOU EVER BEEN DIAGNOSED WITH BODY DYSMORPHIA, OR FELT AS IF THIS IS SOMETHING YOU MIGHT HAVE?',tracking=True)
    dysmorphia_text = fields.Text()
    depression = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='DEPRESSION',tracking=True)
    depression_text = fields.Text()
    care_of_psychiatrist = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                            string='HAVE YOU OR ARE YOU UNDER THE CARE OF A PSYCHIATRIST, PSYCHOLOGIST OR COUNSELLOR?',tracking=True)
    care_of_psychiatrist_text = fields.Text()
    suicide = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                               string='HAVE YOU EVER HAD ANY EPISODE OF SELF HARM OR SUICIDAL TENDENCY?',tracking=True)
    suicide_text = fields.Text()
    contact_hospitalised_patients = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                     string='DO YOU HAVE REGULAR CONTACT WITH HOSPITALISED PATIENTS?',tracking=True)
    contact_hospitalised_patients_text = fields.Text()
    healthcare_worker = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='ARE YOU A HEALTHCARE WORKER?',tracking=True)
    healthcare_worker_text = fields.Text()
    mrsa = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='HAVE YOU EVER BEEN DIAGNOSED OR TREATED FOR MRSA?',tracking=True)
    mrsa_text = fields.Text()
    gp_other_problems = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                         string='DO YOU SEE YOUR GP FOR ANY OTHER PROBLEMS?',tracking=True)
    gp_other_problems_text = fields.Text()
    transgender_programme = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                             string='ARE YOU OR HAVE YOU EVER BEEN ON THE TRANSGENDER PROGRAMME?',tracking=True)
    transgender_programme_text = fields.Text()

    # ALLERGIES OR SENSITIVITIES
    allergies_sensitivities = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                               string='DO YOU HAVE ANY ALLERGIES OR SENSITIVITIES? (Specify and list the reaction)',tracking=True)
    allergies_sensitivities_text = fields.Text()
    allergies_sensitivities_latex = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                     string='DO YOU HAVE AN ALLERGY OR SENSITIVITY ASSOCIATED WITH LATEX (Specify and list the reaction) If you think you have a latex allergy, please note, you will need to supply a blood test to evidence this allergy before we can consider surgery',tracking=True)
    allergies_sensitivities_latex_text = fields.Text()

    # CONFIRMATIONS
    confirm_18_age = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='I CONFIRM THAT I AM OVER 18 YEARS OF AGE',tracking=True)
    confirm_18_age_text = fields.Text()
    confirm_procedure = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                         string='I CONFIRM THAT I BELIEVE THIS PROCEDURE WILL IMPROVE MY HEALTH AND WELLBEING',tracking=True)
    confirm_procedure_text = fields.Text()

    # PATIENT’S MEDICATION QUESTIONNAIRE
    hrt = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='HRT',tracking=True)
    depot_vera = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='DEPOT VERA',tracking=True)
    contraceptive_implant = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='CONTRACEPTIVE IMPLANT',tracking=True)
    coil = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='COIL',tracking=True)
    coc = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='COMBINED CONTRACEPTIVE PILL (COC)',tracking=True)
    mini_pill = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='MINI PILL (PROGESTERONE ONLY)',tracking=True)
    # 91 One2many
    further_information = fields.Char(string='Further Information',tracking=True)
    please_note = fields.Text(string='PLEASE NOTE',tracking=True)

    # Nine Symptom Checklist
    little_interest = fields.Boolean(string='Little interest or pleasure in doing things',tracking=True)
    feeling_down = fields.Boolean(string='Feeling down, depressed, or hopeless',tracking=True)
    sleeping_too_much = fields.Boolean(string='Trouble falling asleep, staying asleep, or sleeping too much',tracking=True)
    feeling_tired = fields.Boolean(string='Feeling tired or having little energy',tracking=True)
    poor_appetite = fields.Boolean(string='Poor appetite or overeating',tracking=True)
    feeling_failure = fields.Boolean(
        string='Feeling bad about yourself, feeling that you are a failure, or feeling that you have let yourself or your family down',tracking=True)
    trouble_concentrating = fields.Boolean(
        string='Trouble concentrating on things such as reading the newspaper or watching television',tracking=True)
    speaking_slowly = fields.Boolean(
        string='Moving or speaking so slowly that other people could have noticed. Or being so fidgety or restless that you have been moving around a lot more than usual',tracking=True)
    hurt_yourself = fields.Boolean(
        string='Thinking that you would be better off dead or that you want to hurt yourself in some way',tracking=True)
    take_care = fields.Boolean(
        string='If you checked off any problem on this questionnaire so far, how difficult have these problems made it for you to do your work, take care of things at home, or get along with other people?',tracking=True)

    # Questionaire
    # <<<<1>>>>
    cloth_fit_your_abdomen = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                               ('somedissatisfied', 'Some What Dissatisfied'),
                                               ('somesatisfied', 'Some What Satisfied'),
                                               ('verysatisfied', 'Very Satisfied')],
                                              string='HOW YOUR CLOTHES FIT YOUR ABDOMEN?',tracking=True)
    size_of_abdomen = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                        ('somedissatisfied', 'Some What Dissatisfied'),
                                        ('somesatisfied', 'Some What Satisfied'),
                                        ('verysatisfied', 'Very Satisfied')],
                                       string='THE SIZE OF YOUR ABDOMEN?',tracking=True)
    side_look_of_abdomen = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                             ('somedissatisfied', 'Some What Dissatisfied'),
                                             ('somesatisfied', 'Some What Satisfied'),
                                             ('verysatisfied', 'Very Satisfied')],
                                            string='HOW YOUR ABDOMEN LOOKS FROM THE SIDE (IE PROFILE VIEW)?',tracking=True)
    shape_of_abdomen = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                         ('somedissatisfied', 'Some What Dissatisfied'),
                                         ('somesatisfied', 'Some What Satisfied'),
                                         ('verysatisfied', 'Very Satisfied')],
                                        string='THE SHAPE OF YOUR ABDOMEN?',tracking=True)
    abdomen_looks_in_swimsuit = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                                  ('somedissatisfied', 'Some What Dissatisfied'),
                                                  ('somesatisfied', 'Some What Satisfied'),
                                                  ('verysatisfied', 'Very Satisfied')],
                                                 string='HOW YOUR ABDOMEN LOOKS IN A SWIMSUIT?',tracking=True)
    toned_your_abdomen_looks = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                                 ('somedissatisfied', 'Some What Dissatisfied'),
                                                 ('somesatisfied', 'Some What Satisfied'),
                                                 ('verysatisfied', 'Very Satisfied')],
                                                string='HOW TONED YOUR ABDOMEN LOOKS?',tracking=True)
    abdomen_looks_when_naked = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                                 ('somedissatisfied', 'Some What Dissatisfied'),
                                                 ('somesatisfied', 'Some What Satisfied'),
                                                 ('verysatisfied', 'Very Satisfied')],
                                                string='HOW YOUR ABDOMEN LOOKS WHEN YOU ARE NAKED?',tracking=True)

    # <<<<2>>>>
    body_looks_when_dressed = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                                ('somedissatisfied', 'Some What Dissatisfied'),
                                                ('somesatisfied', 'Some What Satisfied'),
                                                ('verysatisfied', 'Very Satisfied')],
                                               string='HOW YOUR BODY LOOKS WHEN YOU ARE DRESSED?',tracking=True)
    cloth_fit_to_body = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                          ('somedissatisfied', 'Some What Dissatisfied'),
                                          ('somesatisfied', 'Some What Satisfied'),
                                          ('verysatisfied', 'Very Satisfied')],
                                         string='HOW YOUR CLOTHES FIT YOUR BODY?',tracking=True)
    size_of_body = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                     ('somedissatisfied', 'Some What Dissatisfied'),
                                     ('somesatisfied', 'Some What Satisfied'),
                                     ('verysatisfied', 'Very Satisfied')],
                                    string='THE SIZE (IE WEIGHT) OF YOUR BODY?',tracking=True)
    shape_of_body = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                      ('somedissatisfied', 'Some What Dissatisfied'),
                                      ('somesatisfied', 'Some What Satisfied'),
                                      ('verysatisfied', 'Very Satisfied')],
                                     string='THE SHAPE OF YOUR BODY?',tracking=True)
    body_looks_in_photos = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                             ('somedissatisfied', 'Some What Dissatisfied'),
                                             ('somesatisfied', 'Some What Satisfied'),
                                             ('verysatisfied', 'Very Satisfied')],
                                            string='HOW YOUR BODY LOOKS IN PHOTOS?',tracking=True)
    body_looks_from_behind = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                               ('somedissatisfied', 'Some What Dissatisfied'),
                                               ('somesatisfied', 'Some What Satisfied'),
                                               ('verysatisfied', 'Very Satisfied')],
                                              string='HOW YOUR BODY LOOKS FROM BEHIND?',tracking=True)
    body_looks_from_side = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                             ('somedissatisfied', 'Some What Dissatisfied'),
                                             ('somesatisfied', 'Some What Satisfied'),
                                             ('verysatisfied', 'Very Satisfied')],
                                            string='HOW YOUR BODY LOOKS FROM THE SIDE (IE PROFILE VIEW)?',tracking=True)
    body_looks_summer_cloth = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                                ('somedissatisfied', 'Some What Dissatisfied'),
                                                ('somesatisfied', 'Some What Satisfied'),
                                                ('verysatisfied', 'Very Satisfied')],
                                               string='HOW YOUR BODY LOOKS IN SUMMER CLOTHES(EG SHORTS, T-SHIRTS)?',tracking=True)
    body_looks_in_swimsuit = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                               ('somedissatisfied', 'Some What Dissatisfied'),
                                               ('somesatisfied', 'Some What Satisfied'),
                                               ('verysatisfied', 'Very Satisfied')],
                                              string='HOW YOUR BODY LOOKS IN A SWIMSUIT?',tracking=True)
    body_looks_in_mirror_uncloth = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                                     ('somedissatisfied', 'Some What Dissatisfied'),
                                                     ('somesatisfied', 'Some What Satisfied'),
                                                     ('verysatisfied', 'Very Satisfied')],
                                                    string='HOW YOUR BODY LOOKS IN THE MIRROR UNCLOTHED?',tracking=True)

    # <<<<3>>>>
    shape_of_eyes = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                      ('somedissatisfied', 'Some What Dissatisfied'),
                                      ('somesatisfied', 'Some What Satisfied'),
                                      ('verysatisfied', 'Very Satisfied')],
                                     string='THE SHAPE OF YOUR EYES?',tracking=True)
    attractive_eyes = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                        ('somedissatisfied', 'Some What Dissatisfied'),
                                        ('somesatisfied', 'Some What Satisfied'),
                                        ('verysatisfied', 'Very Satisfied')],
                                       string='HOW ATTRACTIVE YOUR EYES LOOK?',tracking=True)
    alert_eyes = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                   ('somedissatisfied', 'Some What Dissatisfied'),
                                   ('somesatisfied', 'Some What Satisfied'),
                                   ('verysatisfied', 'Very Satisfied')],
                                  string='HOW ALERT (NOT TIRED) YOUR EYES LOOK?',tracking=True)
    open_eyes_look = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                       ('somedissatisfied', 'Some What Dissatisfied'),
                                       ('somesatisfied', 'Some What Satisfied'),
                                       ('verysatisfied', 'Very Satisfied')],
                                      string='HOW OPEN YOUR EYES LOOK?',tracking=True)
    bright_eyes_look = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                         ('somedissatisfied', 'Some What Dissatisfied'),
                                         ('somesatisfied', 'Some What Satisfied'),
                                         ('verysatisfied', 'Very Satisfied')],
                                        string='HOW BRIGHT-EYED YOU LOOK?',tracking=True)
    nice_eyes_look = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                       ('somedissatisfied', 'Some What Dissatisfied'),
                                       ('somesatisfied', 'Some What Satisfied'),
                                       ('verysatisfied', 'Very Satisfied')],
                                      string='HOW NICE YOUR EYES LOOK?',tracking=True)
    youthful_eyes_look = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                           ('somedissatisfied', 'Some What Dissatisfied'),
                                           ('somesatisfied', 'Some What Satisfied'),
                                           ('verysatisfied', 'Very Satisfied')],
                                          string='HOW YOUTHFUL YOUR EYES LOOK?',tracking=True)

    # <<<<4>>>>
    look_in_mirror_cloth = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                             ('somedissatisfied', 'Some What Dissatisfied'),
                                             ('somesatisfied', 'Some What Satisfied'),
                                             ('verysatisfied', 'Very Satisfied')],
                                            string='HOW YOU LOOK IN THE MIRROR CLOTHED?',tracking=True)
    breast_size_match_rest_body = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                                    ('somedissatisfied', 'Some What Dissatisfied'),
                                                    ('somesatisfied', 'Some What Satisfied'),
                                                    ('verysatisfied', 'Very Satisfied')],
                                                   string='HOW YOUR BREAST SIZE MATCHES THE REST OF YOUR BODY?',tracking=True)
    bras_fit = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                 ('somedissatisfied', 'Some What Dissatisfied'),
                                 ('somesatisfied', 'Some What Satisfied'),
                                 ('verysatisfied', 'Very Satisfied')],
                                string='HOW YOUR BRAS FIT?',tracking=True)
    breast_size = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                    ('somedissatisfied', 'Some What Dissatisfied'),
                                    ('somesatisfied', 'Some What Satisfied'),
                                    ('verysatisfied', 'Very Satisfied')],
                                   string='THE SIZE OF YOUR BREASTS?',tracking=True)
    cleavage_when_wear_bra = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                               ('somedissatisfied', 'Some What Dissatisfied'),
                                               ('somesatisfied', 'Some What Satisfied'),
                                               ('verysatisfied', 'Very Satisfied')],
                                              string='HOW MUCH CLEAVAGE YOU HAVE WHEN YOU WEAR A BRA?',tracking=True)
    look_in_mirror_uncloth = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                               ('somedissatisfied', 'Some What Dissatisfied'),
                                               ('somesatisfied', 'Some What Satisfied'),
                                               ('verysatisfied', 'Very Satisfied')],
                                              string='HOW YOU LOOK IN THE MIRROR UNCLOTHED?',tracking=True)

    # <<<<5>>>>
    symmetric_face_look = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                            ('somedissatisfied', 'Some What Dissatisfied'),
                                            ('somesatisfied', 'Some What Satisfied'),
                                            ('verysatisfied', 'Very Satisfied')],
                                           string='HOW SYMMETRIC YOUR FACE LOOKS?',tracking=True)
    balanced_face_look = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                           ('somedissatisfied', 'Some What Dissatisfied'),
                                           ('somesatisfied', 'Some What Satisfied'),
                                           ('verysatisfied', 'Very Satisfied')],
                                          string='HOW BALANCED YOUR FACE LOOKS?',tracking=True)
    well_proportioned_face_look = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                                    ('somedissatisfied', 'Some What Dissatisfied'),
                                                    ('somesatisfied', 'Some What Satisfied'),
                                                    ('verysatisfied', 'Very Satisfied')],
                                                   string='HOW WELL-PROPORTIONED YOUR FACE LOOKS?',tracking=True)
    face_look_at_day_end = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                             ('somedissatisfied', 'Some What Dissatisfied'),
                                             ('somesatisfied', 'Some What Satisfied'),
                                             ('verysatisfied', 'Very Satisfied')],
                                            string='HOW YOUR FACE LOOKS AT THE END OF YOUR DAY?',tracking=True)
    fresh_face_look = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                        ('somedissatisfied', 'Some What Dissatisfied'),
                                        ('somesatisfied', 'Some What Satisfied'),
                                        ('verysatisfied', 'Very Satisfied')],
                                       string='HOW FRESH YOUR FACE LOOKS?',tracking=True)
    rested_face_look = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                         ('somedissatisfied', 'Some What Dissatisfied'),
                                         ('somesatisfied', 'Some What Satisfied'),
                                         ('verysatisfied', 'Very Satisfied')],
                                        string='HOW RESTED YOUR FACE LOOKS?',tracking=True)
    profile_sv_look = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                        ('somedissatisfied', 'Some What Dissatisfied'),
                                        ('somesatisfied', 'Some What Satisfied'),
                                        ('verysatisfied', 'Very Satisfied')],
                                       string='HOW YOUR PROFILE (SIDE VIEW) LOOKS?',tracking=True)
    face_look_in_photo = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                           ('somedissatisfied', 'Some What Dissatisfied'),
                                           ('somesatisfied', 'Some What Satisfied'),
                                           ('verysatisfied', 'Very Satisfied')],
                                          string='HOW YOUR FACE LOOKS IN PHOTOS?',tracking=True)
    face_look_when_wakeup = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                              ('somedissatisfied', 'Some What Dissatisfied'),
                                              ('somesatisfied', 'Some What Satisfied'),
                                              ('verysatisfied', 'Very Satisfied')],
                                             string='HOW YOUR FACE LOOKS WHEN YOU FIRST WAKE UP?',tracking=True)
    face_look_under_bright_light = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                                     ('somedissatisfied', 'Some What Dissatisfied'),
                                                     ('somesatisfied', 'Some What Satisfied'),
                                                     ('verysatisfied', 'Very Satisfied')],
                                                    string='HOW YOUR FACE LOOKS UNDER BRIGHT LIGHTS?',tracking=True)

    # <<<<6>>>>
    width_of_nose_bottom = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                             ('somedissatisfied', 'Some What Dissatisfied'),
                                             ('somesatisfied', 'Some What Satisfied'),
                                             ('verysatisfied', 'Very Satisfied')],
                                            string='THE WIDTH OF YOUR NOSE AT THE BOTTOM (FROM NOSTRIL TO NOSTRIL)?',tracking=True)
    length_of_nose = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                       ('somedissatisfied', 'Some What Dissatisfied'),
                                       ('somesatisfied', 'Some What Satisfied'),
                                       ('verysatisfied', 'Very Satisfied')],
                                      string='THE LENGTH OF YOUR NOSE?',tracking=True)
    bridge_look_nose = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                         ('somedissatisfied', 'Some What Dissatisfied'),
                                         ('somesatisfied', 'Some What Satisfied'),
                                         ('verysatisfied', 'Very Satisfied')],
                                        string='HOW THE BRIDGE OF YOUR NOSE LOOKS (WHERE GLASSES SIT)?',tracking=True)
    nose_suits_face = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                        ('somedissatisfied', 'Some What Dissatisfied'),
                                        ('somesatisfied', 'Some What Satisfied'),
                                        ('verysatisfied', 'Very Satisfied')],
                                       string='HOW WELL YOUR NOSE SUITS YOUR FACE?',tracking=True)
    straight_nose_looks = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                            ('somedissatisfied', 'Some What Dissatisfied'),
                                            ('somesatisfied', 'Some What Satisfied'),
                                            ('verysatisfied', 'Very Satisfied')],
                                           string='HOW STRAIGHT YOUR NOSE LOOKS?',tracking=True)
    size_of_nose = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                     ('somedissatisfied', 'Some What Dissatisfied'),
                                     ('somesatisfied', 'Some What Satisfied'),
                                     ('verysatisfied', 'Very Satisfied')],
                                    string='THE OVERALL SIZE OF YOUR NOSE?',tracking=True)
    shape_of_nose_sv = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                         ('somedissatisfied', 'Some What Dissatisfied'),
                                         ('somesatisfied', 'Some What Satisfied'),
                                         ('verysatisfied', 'Very Satisfied')],
                                        string='THE SHAPE OF YOUR NOSE IN PROFILE (SIDE VIEW)?',tracking=True)
    nose_look_in_photos = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                            ('somedissatisfied', 'Some What Dissatisfied'),
                                            ('somesatisfied', 'Some What Satisfied'),
                                            ('verysatisfied', 'Very Satisfied')],
                                           string='HOW YOUR NOSE LOOKS IN PHOTOS?',tracking=True)
    nose_tip_looks = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                       ('somedissatisfied', 'Some What Dissatisfied'),
                                       ('somesatisfied', 'Some What Satisfied'),
                                       ('verysatisfied', 'Very Satisfied')],
                                      string='HOW THE TIP OF YOUR NOSE LOOKS?',tracking=True)
    nose_look_every_angle = fields.Selection([('verydissatisfied', 'Very Dissatisfied'),
                                              ('somedissatisfied', 'Some What Dissatisfied'),
                                              ('somesatisfied', 'Some What Satisfied'),
                                              ('verysatisfied', 'Very Satisfied')],
                                             string='HOW YOUR NOSE LOOKS FROM EVERY ANGLE?',tracking=True)
