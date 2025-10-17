# -*- coding: utf-8 -*-
{
    'name': 'Dealer Target',
    'version': '17.0',
    'summary': 'Track and manage sales targets for dealers efficiently.',
    'description': 'Manage and track dealer sales targets with automated monitoring, reporting, and integration with sales, accounting, stock, and purchase modules.',
    'author': 'Mastermoon Technologies LLP',
    'depends': ['sale', 'account','mail', 'stock','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/sales_target_views.xml',
    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,
}
