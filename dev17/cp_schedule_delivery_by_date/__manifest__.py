# -*- coding: utf-8 -*-
{
    'name': "Sale Delivery By Scheduled Date",
    'version': '17.0.1.0',
    'category': 'Sales/Sales',
    'summary': "Sale Delivery By Scheduled Date",
    'description': """The Sale Delivery By Scheduled Date module enhances the sales and inventory process by automatically generating and managing delivery orders based on the scheduled delivery date in the sale order. It ensures that all delivery records are accurately reflected in the Stock Move History menu, providing a clear and organized overview of stock movements related to sale orders. This feature improves order tracking and inventory management by linking sales and stock operations efficiently.""",
    'author': "CPFreelancer",
    'license': 'OPL-1',
    'depends': ['sale_management','sale_stock'],
    'data': [
        'views/sale_order_views.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'currency': 'EUR',
    'price': '20',
}
