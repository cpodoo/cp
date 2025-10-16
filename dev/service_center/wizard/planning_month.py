from odoo import fields,api,models
from datetime import datetime
from dateutil import relativedelta

class Planning_Month(models.TransientModel):
    _name = 'planning.month'

    date_start=fields.Date(string='Start Date')
    date_end=fields.Date(string='End Date')
    planning_month = fields.Char(string="Planning Month", store=True)


    def create_planning(self):

        diff = relativedelta.relativedelta(self.date_end, self.date_start)
        months = diff.years * 12 + diff.months + (1 if diff.days > 0 else 0)
        self.planning_month = months

        context = self.env.context
        active_id = context.get('active_id')
        if active_id:
            service_request = self.env['service.request'].browse(active_id)
            service_request.planning_month = self.planning_month

        # return {'type': 'ir.actions.act_window_close'}


