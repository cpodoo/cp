# -*- coding: utf-8 -*-
{
    'name': 'Asset Customization',
    'version': '1.0',
    'depends': ['base', 'stock', 'purchase', 'product', 'account_asset', 'point_of_sale'],
    'author': '',
    'category': 'Asset',
    'description': 'Manage company assets with serial tracking and purchase linking',
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'views/inspection_order_views.xml',
        'views/maintenance_order_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}
