# -*- coding: utf-8 -*-
{
    'name': 'Final Price',
    'version': '1.0',
    'summary': 'Control final price visibility on reports',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'reports/report.xml',
        'reports/report_saleorder_inherit.xml',
        'reports/report_retail_bill.xml',
        'reports/mobile_sell_bill_template.xml',
        'reports/mobile_sell_bill_report.xml',
        'views/sale_order_view.xml',
        'views/mobile_sell_bill_views.xml',
        'views/mobile_sell_bill_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
