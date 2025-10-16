# -*- coding: utf-8 -*-
{
    "name": "Product Brand Management",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "summary": "Manage product brands and integrate branding into sales and marketplace operations.",
    "description": """
Product Brand Management
========================

This module allows Odoo users to define and manage product brands efficiently. It provides seamless integration of brand information into:

- Product templates
- Inventory Product Brand
- Seller Dashboard

Key Features:
-------------
- Create and manage product brand records
- Assign brands to products easily
- Track inventory by product brand
- Showcase brand information in Odoo Marketplace seller dashboards
- Improve product search and filtering based on brand

""",
    "author": "",
    "website": "",
    "license": "LGPL-3",
    "depends": [
        "stock",
        "sale",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_brand_views.xml",
        "views/product_template_views.xml",
        "views/sale_report_views.xml",
        # "views/product_brand_templates.xml",
        "views/menu.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}