from odoo import models, fields


class PostOpWound(models.Model):
    _name = "postop.wound"
    _description = "Surgery Post-Op Wound"

    name = fields.Char(default='Post-Op Wound',tracking=True)
    creation_date = fields.Date(string='Creation Date',tracking=True)
    # 2 one2many
    special_notes = fields.Text(string='Special Instructions / Notes',tracking=True)
    pre_op_checked = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Pre op Notes Checked',tracking=True)
    pre_op_checked_char = fields.Char()
    bleeding_absence = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Absence of Bleeding',tracking=True)
    bleeding_absence_char = fields.Char()
    wound_closed = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Wound closed',tracking=True)
    wound_closed_char = fields.Char()
    no_wound_edge = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='No wound edge Inflammation',tracking=True)
    no_wound_edge_char = fields.Char()
    granulating = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Granulating',tracking=True)
    granulating_char = fields.Char()
    infection_occuring = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Infection Occurring',tracking=True)
    infection_occuring_char = fields.Char()
    action_required = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Action Required',tracking=True)
    action_required_char = fields.Char()
    reported_to = fields.Many2one('hr.employee', string='Reported to',tracking=True)
    date_time = fields.Datetime(string='Date Time',tracking=True)
    photos_complete = fields.Many2many('ir.attachment', string="Photos Complete",tracking=True)

