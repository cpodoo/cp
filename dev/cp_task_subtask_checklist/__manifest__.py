# -*- coding: utf-8 -*-

{
    'name': 'Cp Project Task SubTask Checklist',
    'version': '18.0.1.0.0', 
    'author': 'Cp',
    'category': 'Project',
    'summary': 'Add checklists with activities to project tasks. Track progress and restrict stage changes based on checklist completion. Task Subtask Checklist.',
    'description': """
Added CheckList And CheckList Related Features Into Project (Odoo 18 Version)
------------------------------------------------------------------------------
With the help of this module you can divide tasks or sub-tasks into lists of activities, so task and subtask progress can be easily controlled in Odoo project management.

Key features:
-------------
*   Any Number Of Configurable Checklists (General or Project Specific)
*   Configurable Checklist Stages (Default 3 Stages; you can add more stages).
*   Only Admin And Manager Can Add/Remove Checklists.
*   Any Number Of Checklist Activities per Task.
*   Set Color Based on Checklist Activity Stage (via view modifications if needed, base logic supports stages).
*   Separate Checklist Activity Menu With Different Filter/Group By Options.
*   Complete / Cancel Checklist Activities in Bulk.
*   Checklist Progress Gauge/Bar in Task Kanban, List, and Form Views.
*   Activities Can Be Checked/Managed From Task Form View.
*   Restrict Task Progress (stage change) until all associated checklist items are either Canceled Or Completed.

    """,
    'depends': ['base','project', 'web', 'mail'],
    'data': [
        'security/checklist_security.xml',
        'security/ir.model.access.csv',
        'views/res_config_view.xml',
        'views/views.xml',
        'data/checklist_data.xml',
        'wizard/activity_approve_reject_view.xml',
    ],
    'license': 'OPL-1',
    'application': True,
    'installable': True,
    'auto_install': False,
}