from odoo import fields, api, models, _
from datetime import date
from odoo.exceptions import ValidationError

class srWarrantyReportWizard(models.TransientModel):
    _name = "sr.warranty.report.wizard"
    _description = "Warranty Report"

    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    state = fields.Selection(
        [("in_warranty", "In Warranty"), ("expired_warranty", "Expired Warranty")]
    )

    # Start date validation function
    @api.onchange("start_date")
    def _end_date_onchange(self):
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError(_("Please select the correct start date."))

    # End date validation function
    @api.onchange("end_date")
    def _start_date_onchange(self):
        if self.start_date and self.start_date > self.end_date:
            raise ValidationError(_("Please select the correct end date."))

    def print_pdf_report(self):
        data = {}
        report_action = self.env.ref(
            "cp_warranty_management.sr_product_warranty_report_action"
        ).report_action(self, data=data)

        report_action["close_on_report_download"] = True  

        return report_action
