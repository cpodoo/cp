# -*- coding: utf-8 -*-
{
    'name': " Cp New Notification ",
    'version': '17.0.1.0',
    'summary': 'Displays popup notifications to specific users.',
    'description': """
         Allows administrators to create notifications that appear as popups for selected users upon login or page refresh.
    """,
    'category': 'Tools',
    'license': 'OPL-1',
    'depends': ['web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'views/template.xml',
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'cp_new_notification/static/src/scss/style.scss',
            'cp_new_notification/static/src/xml/notification_dialog.xml',
            'cp_new_notification/static/src/js/notification_popup_service.js',
        ],
    },
    'sequence': 1,
    'installable': True,
    'application': True, 
    'price': 0,
    'currency': 'EUR',
}
