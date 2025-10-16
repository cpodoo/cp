# -- coding: utf-8 --
{

    'name': 'MR CUSTOM',
    'version': '18.0.1.0',
    'summary': '',
    'description': '',
    'author': 'Mastermoon Technologies LLP',
    'category': '',
    'depends': ['base', 'stock', 'contacts', 'product', 'uom'],
    'license': 'OPL-1',

    'data': [
        'security/ir.model.access.csv',
        'views/mr_custom_views.xml',
        'data/mr_custom_sequence.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
