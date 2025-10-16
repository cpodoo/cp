# -*- coding: utf-8 -*-

{
    'name': "Hospital Management",
    'summary': """Odoo Hospital Management to manage all your operations with billing""",
    'description': """
       Hospital Management System
Resource
Health center
health center building
health center ward
health center beds
health center ot 
health center pharmacy
health center domiciliary unit
Patients
inpatients
inpatients addmission
vaccine
physician
appointments
prescription
evaluation
lab test
surgery
newborn
insurance
imaging test
medicine
pathology


    """,
	'author' : 'MasterMoon Technologiess LLP',
    'category': 'Medical',
    'version': '18.0.1.0',
    "price": "150.00",
    "currency": "EUR",
    'images': ['static/description/Banner.gif'],
    
    'depends': ['purchase','stock','hr','sale','sale_management','account','mrp','uom','l10n_us','product',
                'crm','web'
    ],
    'data': [
        'data/ir_sequence_data.xml',
        'data/product.xml',
        'security/hospital_management_security.xml',
        'security/ir.model.access.csv',
        'wizard/test_invoice_advance_views.xml',
        'views/menu.xml',
        'views/health_center.xml',
        'views/health_center_building.xml',
        'views/health_center_ward.xml',
        'views/health_center_beds.xml',
        'views/health_center_ot.xml',
        'views/health_center_pharmacy.xml',
        'views/health_center_domiciliary_unit.xml',
        'views/patient.xml',
        'views/inpatient_admissions.xml',
        'views/vaccine.xml',
        'views/call_log.xml',
        'views/physician.xml',
        'views/appointment.xml',
        'views/prescription.xml',
        'views/evaluation.xml',
        'views/lab_tests.xml',
        'views/surgery.xml',            
        'views/newborn.xml',
        'views/insurance.xml',
        'views/imaging_test.xml',
        'views/medicine.xml',
        'views/pathology.xml',
        'views/allergy.xml',
        'views/consultation.xml',
        'views/doctor.xml',
        'views/degree.xml',
        'views/customer_group.xml',
        'views/customer_type.xml',
        'views/doctor_membership.xml',
        'views/mail_template.xml',
        'views/nurse.xml',
        'views/patient_ethnic_grp.xml',
        'views/procedure.xml',
        'views/res_partner.xml',
        'views/role.xml',
        'views/speciality.xml',
        'views/surgery.xml',
        # 'views/attachments.xml',
        'views/vendor_type.xml',
        # 'views/postop.xml',
        # 'views/preop.xml',
        'reports/report_out_patient_templates.xml',
        'reports/report_in_patient_templates.xml',
        'reports/report_appointment_templates.xml',
        'reports/report_prescription_templates.xml',
        'reports/report_surgery_templates.xml',
        'reports/report_lab_tests_templates.xml',
        'reports/report_doctor_templates.xml',
        'reports/report_nurse_templates.xml',
        'reports/report.xml',
    ],
    'demo': [
        'demo/product.xml',
        'demo/health_center_demo.xml',
        'demo/inpatient_demo.xml',
        'demo/medicine_vaccine_data.xml',
        'demo/call_log_demo.xml',
        'demo/appointment_prescription_evaluation_demo.xml',
        'demo/surgery_demo.xml',
        'demo/lab_test_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'cp_hospital_management/static/src/css/hospital.css',
        ],
    },
    'installable': True,
    'auto_install': False,
}