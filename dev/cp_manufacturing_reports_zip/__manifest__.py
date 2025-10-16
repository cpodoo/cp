# -*- coding: utf-8 -*-
{
    'name': 'Manufacturing Orders Reports(ZIP)',
    'version': '18.0.1.0',
    'summary': 'Manufacturing Reports Zip',
    'description': "The Manufacturing Reports Zip module streamlines report management by bundling selected manufacturing reports into a downloadable zip file. This feature enhances productivity and provides quick access to essential manufacturing data, making it easier to analyze and manage operations efficiently.",
    'category': 'Manufacturing/Manufacturing',
    'license': 'OPL-1',
    'author': 'CP-Freelancer',
    'depends': ['mrp', 'report_xlsx'],
    'data': [
        'data/server_action_data.xml',
        'views/mo_report_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'currency': 'EUR',
    'price': '25',
}