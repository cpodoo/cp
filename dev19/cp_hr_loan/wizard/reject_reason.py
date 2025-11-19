# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class RejectReasonWizard(models.TransientModel):
    _name = 'reject.reason'
    _description = 'Reject Reasons From The Company Side'

    loan_id = fields.Many2one('employee.loan', string="Loan", required=True, readonly=True, help="Reference to Employee Loan")
    reason = fields.Text(string="Reject Reason", required=True)

    def action_reject_loan(self):
        self.ensure_one()

        if not self.loan_id:
            raise UserError(("Cannot process rejection without a linked loan."))

        if not self.loan_id.employee_id or not self.loan_id.employee_id.work_email:
            
             self.loan_id.reject_reason = self.reason
             self.loan_id.state = 'reject'
             return {'type': 'ir.actions.act_window_close'}

        rejection_source = self.env.context.get('rejection_source') 
        template_xml_id = None

        if rejection_source == 'manager':
            template_xml_id = 'cp_hr_loan.cp_loan_manager_reject'
           
        elif rejection_source == 'hr':
            template_xml_id = 'cp_hr_loan.hr_loan_manager_reject_loan'
            if not self.loan_id.hr_manager_id:
                hr_user_employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
                if hr_user_employee:
                    self.loan_id.hr_manager_id = hr_user_employee
        else:
             raise UserError(("Could not determine who is rejecting the loan. Rejection source is missing or invalid."))

        self.loan_id.reject_reason = self.reason
        self.loan_id.state = 'reject'

        if template_xml_id:
            mail_template = self.env.ref(template_xml_id, raise_if_not_found=False)
            if mail_template:
                email_values = {
                    'email_to': self.loan_id.employee_id.work_email,
                }
                try:
                     mail_template.send_mail(
                         self.loan_id.id,
                         email_values=email_values,
                         force_send=True 
                     )
                except Exception as e:
                    self.env.user.notify_danger(message=("Loan was rejected, but the notification email could not be sent.\nPlease check Mail Server configuration and template '%s'.\nError: %s", template_xml_id, e))
            else:
                 raise UserError(("The loan was rejected, but the notification email template ('%s') could not be found.", template_xml_id))

        return {'type': 'ir.actions.act_window_close'}  



# #-*- coding: utf-8 -*-

# from odoo import models, fields


# class RejectReasonWizard(models.TransientModel):
#     _name = 'reject.reason'
#     _description = 'Reject Reasons From The Company Side'

#     loan_id = fields.Many2one('employee.loan', string="Loan", help="Reference to Employee Loan")  
#     reason = fields.Text(string="Reject Reason", required=True)

#     def action_reject_loan(self):
#         """ Reject the loan and send a rejection email """
#         self.ensure_one()
#         if self.loan_id:
#             self.loan_id.reject_reason = self.reason  # Save reason to loan
#             self.loan_id.state = 'reject'  # Update loan state to rejected (if applicable)

#             # Send rejection email
#             mail_template = self.env.ref('cp_hr_loan.cp_manager_reject_loan', raise_if_not_found=False)
#             if mail_template:
#                 mail_template.send_mail(self.loan_id.id, force_send=True)

#         return {'type': 'ir.actions.act_window_close'}  # Close wizard
