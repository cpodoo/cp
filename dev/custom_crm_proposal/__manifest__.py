# -*- coding: utf-8 -*-
{
    'name': 'CRM Customization Praposal',
    'version': '18.0',
    'sequence': 1,
    'category': 'Generic Modules/Tools',
    'description':
        """
        This module adds the following functionality to the Odoo CRM customization process for handling Business Proposals:

- Manage Business Proposals with auto-generated Proposal IDs and MoU IDs
- Capture key proposal details: Proposal Date, MoU Date, and related identifiers
- Include a Deliverables tab with line items for:
  - Serial number
  - Year
  - Item and Description
  - Quantity and Unit of Measure
  - Display control (only show selected items in print view)
- Seamless sequence generation for Business Proposal and MoU IDs
- Ready for customization and print integration

Ideal for teams managing structured proposals, deliverables, installment under a CRM workflow.

    """,
    'category': 'Sales/CRM',
    'depends': ['product', 'crm', 'sale_crm', 'account'],
    'data': [
        'data/sequence.xml',
        'data/stage.xml',
        'security/ir.model.access.csv',
        'reports/proposal_template_report.xml',
        'reports/mou_report.xml',
        'reports/report.xml',
        'views/crm_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}