{
    "name": "Property Management",
    "version": "18.0",
    "summary": "Manage Properties, Offers, Contractors, and Payments",
    "description": """
The One and Only Best Property Management System Available on Odoo!

This module allows you to efficiently manage real estate properties along with their details like tags, types, offers, client budgets, and contractors.

Key Features:
- Create and manage properties with custom tags and property types
- Track offers from clients and associated budgets
- Manage property-related contractors and their details
- Record and monitor property-related payments
- Configurable menu and sequence settings for smooth operations
    """,
    "author": "",
    "website": "https://www.odoo.com",
    "category": "Real Estate",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "data/property_management_sequence.xml",
        "views/property_management_contractor_views.xml",
        "views/property_management_payment_views.xml",
        "views/property_management_offer_views.xml",
        "views/property_management_tag_views.xml",
        "views/property_management_type_views.xml",
        "views/property_management_views.xml",
        "views/property_menus.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "auto_install": False,
}
