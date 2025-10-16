# -*- coding: utf-8 -*-
{
    'name': 'Dealer Target',
    'version': '18.0.1.0',
    'summary': 'Track and manage sales targets for dealers efficiently.',
    'description': 'Manage and track dealer sales targets with automated monitoring, reporting, and integration with sales, accounting, stock, and purchase modules.',
    'license': 'OPL-1',
    'author': 'CP-Freelancer',
    'category': 'Sales/Sales',
    'depends': ['sale', 'account', 'mail', 'stock', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/sales_target_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}