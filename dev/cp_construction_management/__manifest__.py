# -*- coding: utf-8 -*-

{
    'name' : 'Construction Management',
    'version': '18.0.1.0',
    'price': 79.0,
    'currency': 'EUR',
        'license': 'Other proprietary',

    'author': 'MasterMoon Technologies Ltd.',
    'images': ['static/description/img1.jpg'],
    'category': 'Project',
    'summary':  """This module provide Construction Management Related Activity.""",
    'description': """

This module provide Construction Management Related Activity.
Construction
Construction Projects
Budgets
Notes
Materials
Material Request For Job Orders
Add Materials
Job Orders
Create Job Orders
Job Order Related Notes
Issues Related Project
Vendors
Vendors / Contractors

Construction Management
Construction Activity
Construction Jobs
Job Order Construction
Job Orders Issues
Job Order Notes
Construction Notes
Job Order Reports
Construction Reports
Job Order Note
Construction app
Construction
job costing
job cost sheet
job contracting
Construction Management

This module provide feature to manage Construction Management activity.
Menus:
Construction
Construction/Configuration
Construction/Configuration /Stages
Construction/Construction
Construction/Construction/Budgets
Construction/Construction/Notes
Construction/Construction/Projects
Construction/Job Orders
Construction/Job Orders /Issues
Construction/Job Orders /Job Orders
Construction/Job Orders /Notes
Construction/Materials / BOQ
Construction/Materials /Material Requisitions / BOQ
Construction/Materials /Materials
Construction/Vendors
Construction/Vendors /Contractors
Defined Reports
Notes
Project Report
Task Report
Construction Project - Project Manager
real estate property
propery management
bill of material
Material Planning On Job Order

Bill of Quantity On Job Order
Bill of Quantity construction
    """,
    'depends': ['project',
                'stock',
                'stock_account',
                'purchase',
                'hr_timesheet',
                ],
    'data': [
            'security/construction_security.xml',
            'security/ir.model.access.csv',
            'views/construction_management_view.xml',
            'views/project_task_view.xml',
            'views/project_view.xml',
            'views/report_noteview.xml',
            'views/report_reg.xml',
            'views/project_report.xml',
            'views/task_report.xml',
            'views/purchase_view.xml',
            'views/stock_picking.xml',
            'views/product_view.xml',
            'views/account.xml',
        ],
    'installable' : True,
    'application' : True,
    'auto_install' : False,
}

