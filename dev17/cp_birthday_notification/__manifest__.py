# -*- coding: utf-8 -*-

{
    'name': 'Cp Birthday Notification',
    'version': '17.0',
    'category': 'Tools',
    'depends': ['base_setup', 'hr', 'contacts'],
    'license': 'OPL-1',
    'author': 'MasterMoon Technology LLP.',
    'website': '',
    'summary': 'Birthday Wishes to Employees & Contacts',
    'description': """
        This module send email notification for birthday wish to employees and contacts. | Birthday blessings. |Birthday card. | Birthday cheer. | Birthday notification. | Birthday greeting. | Birthday message. | Birthday reminder. | Birthday wishes. | Bliss. | Email notification. | Joyous occasion. | Moment. |Special day. | Wishes. | Your day.
    """,
    'images': [],
    'data': [
        'data/mail_data.xml',
        'data/cron_data.xml',
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
