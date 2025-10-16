from odoo import fields,api,models

class TestModelWizard(models.TransientModel):
    _name =  'test.model.wizard'
    _description = 'Test Model Wizard'

    test_field = fields.Char(string = 'Test Field')
