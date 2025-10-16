# -*- coding: utf-8 -*-
{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Properties',
    'description': 'A module to handle property listings, sales, and customer management.',
    'author': 'Qnomix Tech',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/real_estate_views.xml',
    ],
    'installable': True,
    'application': True,  # This makes the module appear in the 'Apps' filter
}