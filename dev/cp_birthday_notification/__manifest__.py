# -*- coding: utf-8 -*-

{
    'name': 'cp Birthday Notification',
    'version': '18.0.1.0',
    'category': 'Tools',
    'summary': 'Birthday Wishes to Employees & Contacts',
    'description': """
        This module sends automated birthday email notifications to Employees and Contacts.

        Features:
            - Automatically detects birthdays for contacts and employees
            - Sends email greetings on their birthday
            - Includes configuration settings in General Settings

        Ideal for improving engagement and culture.
    """,
    'depends': ['hr', 'contacts'],
    'license': 'OPL-1',
    'author': 'CP-Freelancer',
    'data': [
        'data/mail_data.xml',
        'data/cron_data.xml',
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
