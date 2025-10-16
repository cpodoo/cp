from odoo import models, fields

class ProductCreateWizard(models.TransientModel):
    _name = 'product.create.wizard'
    _description = 'Create Coffee & Tea Products'

    def action_create_products(self):
        product_data = [
            # ☕ Coffee & Beverages
            {
                'name': 'Espresso Coffee Beans',
                'default_code': 'COF-ESP-001',
                'uom_xml_id': 'uom.product_uom_kgm',
                'list_price': 300.00,
                'standard_price': 180.00,
                'description': 'Strong roasted beans for espresso',
            },
            {
                'name': 'Cold Brew Coffee (Bottle)',
                'default_code': 'COF-COLD-002',
                'uom_xml_id': 'uom.product_uom_ltr',
                'list_price': 180.00,
                'standard_price': 90.00,
                'description': 'Ready-to-drink cold brew coffee',
            },
            {
                'name': 'Ground Coffee – 500g Pack',
                'default_code': 'COF-GRD-001',
                'uom_xml_id': 'uom.product_uom_kgm',
                'list_price': 150.00,
                'standard_price': 80.00,
                'description': 'Medium roast ground coffee',
            },
            {
                'name': 'Coffee Capsules – 10 Pack',
                'default_code': 'COF-CAP-010',
                'uom_xml_id': 'uom.product_uom_unit',
                'list_price': 200.00,
                'standard_price': 100.00,
                'description': 'Coffee capsules for machines',
            },
            # 🍵 Tea Products
            {
                'name': 'Green Tea Pack – 100g',
                'default_code': 'TEA-GRN-001',
                'uom_xml_id': 'uom.product_uom_gram',
                'list_price': 120.00,
                'standard_price': 60.00,
                'description': 'Refreshing loose leaf green tea',
            },
            {
                'name': 'Herbal Infusion – 250ml',
                'default_code': 'TEA-HERB-250',
                'uom_xml_id': 'uom.product_uom_ml',
                'list_price': 90.00,
                'standard_price': 45.00,
                'description': 'Ready-to-drink herbal tea',
            },
            {
                'name': 'Masala Chai Powder – 1kg',
                'default_code': 'TEA-MAS-001',
                'uom_xml_id': 'uom.product_uom_kgm',
                'list_price': 280.00,
                'standard_price': 160.00,
                'description': 'Spiced tea powder',
            },
        ]

        for data in product_data:
            uom = self.env.ref(data['uom_xml_id'], raise_if_not_found=False)
            if not uom:
                continue

            self.env['product.template'].create({
                'name': data['name'],
                'default_code': data['default_code'],
                'uom_id': uom.id,
                'uom_po_id': uom.id,
                'list_price': data['list_price'],
                'standard_price': data['standard_price'],
                'type': 'consu',
                'description': data['description'],
            })

