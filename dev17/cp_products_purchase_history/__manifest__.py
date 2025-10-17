# -- coding: utf-8 --

{
    'name': ' CP Products Purchase History',
    'version': '17.0.1.0',
    'category': 'Purchase',
    'summary': 'Tracks and displays the purchase history of products in purchase orders',
    'description': 'This module adds functionality to view the product purchase history directly from the purchase order lines.',
    'license': 'OPL-1',
    'author': 'CP-Freelancer',
    'category': 'Purchase/Purchase',
    'depends': ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}