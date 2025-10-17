# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class SkipInstallmentRejectReasonWizard(models.TransientModel):
    _name = 'skip.installment.reject.reason'
    _description = 'Skip Installment Rejection Reason'

    skip_installment_id = fields.Many2one(
        'cp.skip.installment',
        string="Skip Installment Request",
        required=True,
        readonly=True,
        help="Reference to the Skip Installment Request being rejected"
    )
    reason_text = fields.Text(string="Reject Reason", required=True)

    def action_reject_skip_installment(self):
        self.ensure_one()

        try:
            self.skip_installment_id.write({
                'reject_reason': self.reason_text,
                'state': 'reject'
            })
        except Exception as e:
            raise UserError("Failed to update the skip installment state/reason_text. Error: %s" % e)

        skip_request = self.skip_installment_id
        if not skip_request.employee_id or not skip_request.employee_id.work_email:
             self.env.user.notify_warning(
                 message="Skip Installment request '%(req_name)s' rejected. Notification email skipped: Employee '%(emp_name)s' has no work email." % {
                     'req_name': skip_request.name,
                     'emp_name': skip_request.employee_id.name
                 }
             )
             return {'type': 'ir.actions.act_window_close'}

        rejection_source = self.env.context.get('rejection_source')
        template_xml_id = None

        if rejection_source == 'manager':
            template_xml_id = 'cp_hr_loan.cp_manager_reject_skip_installment'
        elif rejection_source == 'hr':
            template_xml_id = 'cp_hr_loan.hr_manager_reject_skip_installment'
            if not skip_request.hr_manager_id:
                hr_user_employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
                if hr_user_employee:
                    skip_request.hr_manager_id = hr_user_employee
        else:
             raise UserError("Could not determine who is rejecting the skip request. Rejection source ('%s') is missing or invalid." % rejection_source)

        if template_xml_id:
            mail_template = self.env.ref(template_xml_id, raise_if_not_found=False)
            if mail_template:
                email_values = {'email_to': skip_request.employee_id.work_email}
                try:
                     mail_template.send_mail(
                         skip_request.id,
                         email_values=email_values,
                         force_send=True
                     )
                except Exception as e:
                    self.env.user.notify_danger(
                        message="Skip request rejected, but email failed. Template: %(template)s. Error: %(error)s" % {
                            'template': template_xml_id,
                            'error': e
                        }
                    )
            else:
                 raise UserError("The skip rejection email template '%s' could not be found." % template_xml_id)

        return {'type': 'ir.actions.act_window_close'}