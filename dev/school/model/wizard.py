from odoo import models, fields, api


class PlanningWizard(models.TransientModel):
    _name="planning.wizard"
    _description="Planning Wizard"

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    num_days = fields.Integer(string="Number of days", compute="_compute_num_days")

    @api.depends('start_date','end_date')
    def _compute_num_days (self):
        for record in self:
            if record.start_date and record.end_date:
                delta=record.end_date-record.start_date
                record.num_days = (delta.days+1)
            else :
                record.num_days=0

    def generate_planning(self):
        num_days = self.num_days
        print("Number of days", num_days)

    def cancel(self):
        return {'type': 'ir.actions.act_window_close'}

    def open_planning_wizard(self):
        return{'type': 'ir.actions.act_window',
               'name': 'Planning Wizard',
               'res_model': 'planning.wizard',
               'view_mode': 'form',
               'target': 'new'}