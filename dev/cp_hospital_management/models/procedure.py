# -*- coding: utf-8 -*-


from odoo import models, fields ,api


class Procedure(models.Model):
    _name = "procedure"
    _description = "Medical Procedure"
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    name = fields.Char('Procedure',tracking=True)
    avg_time = fields.Float(string='Average Time',tracking=True)
    avg_time_uom_id = fields.Many2one('uom.uom',string='Average Time Unit',tracking=True)

    max_time = fields.Float(string='Max Time',tracking=True)
    max_time_uom_id = fields.Many2one('uom.uom',string='Max Time Unit',tracking=True)

    min_time = fields.Float(string='Min Time',tracking=True)
    min_time_uom_id = fields.Many2one('uom.uom',string='Min Time Unit',tracking=True)

    min_bmi = fields.Float(string='Min Bmi',tracking=True)
    min_bmi_uom_id = fields.Many2one('uom.uom',string='Min Bmi Unit',tracking=True)

    max_bmi = fields.Float(string='Max Bmi',tracking=True)
    max_bmi_uom_id = fields.Many2one('uom.uom',string='Max Bmi Unit',tracking=True)

    doc_role_ids = fields.Many2many('role.data','procedure_doc_table_rel','procedure_id','doc_role_id',domain=[('type','=','doc')],string='Doctor Role Type',tracking=True)
    nurse_role_ids = fields.Many2many('role.data','procedure_nurse_table_rel','procedure_id','nurse_role_id',domain=[('type','=','nurse')],string='Nurse Role Type',tracking=True)
    special_equip_ids = fields.Many2many('product.product','procedure_product_table_rel','procedure_id','product_id',string='Special Equipment Required',tracking=True)
    instrument_set_ids = fields.Many2many('mrp.bom','procedure_instrument_set_rel','procedure_id','mrp_bom_id',string='Instruments Set',tracking=True)
    # fields.many2many('other.object.name', 'relation object', 'actual.object.id', 'other.object.id', 'Field Name')
    procedure_line_id = fields.One2many('procedure.lines','procedure_id',string='Operating Theatre',tracking=True)
    avg_time_actual = fields.Float(string='Average Time Actual',tracking=True)

    @api.onchange('avg_time')
    def get_avg_time_actual(self):
        if self.avg_time:
            self.avg_time_actual = self.avg_time
        else:
            self.avg_time_actual = ''


class ProcedureLines(models.Model):
    _name = 'procedure.lines'
    _description = 'Procedure lines'

    room_id = fields.Many2one('health.center.ot',string='Operating Theatre',tracking=True)
    centre_id = fields.Many2one('health.center',string='Surgical Centre',tracking=True)
    building_id = fields.Many2one('health.center.building',string='Building',tracking=True)
    procedure_id = fields.Many2one('procedure',string='Procedure',tracking=True)

