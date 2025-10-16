# -- coding: utf-8 --

{
    'name': 'Purchase & Sale Orders Line Images and Sequence',
    'version': '18.0.1.0',
    'summary': 'Optimize Sale and Purchase Orders with automatic sequence numbering and product images in order lines. Improve order visibility, streamline tracking, and enhance accuracy with a structured and visually intuitive interface. Fully integrated with Odoo’s sale and purchase workflow, including PDF reports with images and sequence numbers.',
    'description': 'This module enhances the Sale and Purchase Order functionality in Odoo by adding sequence numbers and product images to order lines, improving clarity and efficiency in purchase management. It automatically assigns sequence numbers to each sale and purchase order line for better tracking and organization while displaying product images directly within order lines for easy visual identification. Users can reorder lines dynamically using drag-and-drop sequence management. The module also integrates with Odoo’s PDF reporting system. Additionally, it offers configurable settings to enable or disable product images, ensuring flexibility in sale and purchase management. Fully integrated with Odoo’s sale and purchase workflow, this module streamlines operations by making order lines more structured, visually informative, and exportable as PDF reports.',
    'license': 'OPL-1',
    'author': 'CP-Freelancer.',
    'category': 'Sales/Purchase',
    'depends': ['sale_management', 'purchase'],
    'data': [
        'views/sale_order_line_views.xml',
        'views/purchase_order_line_views.xml',
        'views/res_config_settings_sale_views.xml',
        'views/res_config_settings_purchase_views.xml',
        'report/sale_order_report.xml',
        'report/purchase_order_report.xml',
    ],
    'installable': True,
    'application': False,
    'price': 30,
    'currency': 'EUR',
}