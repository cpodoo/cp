# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.tools.translate import html_translate
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class UserNotification(models.Model):
    _name = 'user.update.notification'
    _description = 'User Update Notification Link'
    _order = 'create_date desc'

    user = fields.Many2one('res.users', string="User", required=True, ondelete='cascade', index=True)
    useraction = fields.Selection([('new', 'New'), ('closed', 'Closed')], string="Status", default="new", required=True)
    notification_id = fields.Many2one('new.update.notification', string="Notification", required=True,
                                      ondelete='cascade', index=True)

    _sql_constraints = [
        ('user_notification_uniq', 'unique (user, notification_id)',
         'A user can only be linked to the same notification once.')
    ]


class NewNotification(models.Model):
    _name = 'new.update.notification'
    _description = 'New Update Notification Content'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string="Title", required=True, tracking=True)
    description = fields.Html(
        string="Content",
        sanitize_attributes=False,
        translate=html_translate,
        sanitize_form=False,
        required=True
    )
    state = fields.Selection([
        ('new', 'Draft'),
        ('confirm', 'Active'),
        ('done', 'Closed')
    ], string="State", default='new', required=True, tracking=True, copy=False, index=True)

    user_notification_ids = fields.One2many(
        'user.update.notification', 'notification_id',
        string="Assigned Users",
        copy=False
    )

    show_set_draft_button = fields.Boolean(compute='_compute_show_buttons')
    show_set_confirm_button = fields.Boolean(compute='_compute_show_buttons')
    show_set_done_button = fields.Boolean(compute='_compute_show_buttons')

    @api.depends('state')
    def _compute_show_buttons(self):
        for rec in self:
            rec.show_set_draft_button = rec.state in ['confirm', 'done']
            rec.show_set_confirm_button = rec.state == 'new'
            rec.show_set_done_button = rec.state == 'confirm'

    def set_draft(self):
        self.user_notification_ids.write({'useraction': 'new'})
        self.write({'state': 'new'})

    def set_confirm(self):
        template_id = self.env.ref('mtech_new_notification_HH.email_template_new_notification',
                                   raise_if_not_found=False)

        _logger.warning("!!! DEBUG: set_confirm method called !!!")

        records_to_confirm = self.filtered(lambda r: r.state == 'new')
        if not records_to_confirm:
            _logger.warning("!!! DEBUG: No records found in 'new' state to confirm. !!!")
            return True

        try:
            records_to_confirm.write({'state': 'confirm'})
            _logger.warning(f"!!! DEBUG: State successfully written to 'confirm' for IDs: {records_to_confirm.ids} !!!")
        except Exception as e:
            _logger.error(f"!!! DEBUG: ERROR during state write: {str(e)} !!!")
            raise UserError(f"ERROR during state write: {str(e)}")

        # Send mail to each user
        if template_id:
            for record in records_to_confirm:
                for user_notification in record.user_notification_ids:
                    if user_notification.user and user_notification.user.partner_id.email:
                        email_to = user_notification.user.partner_id.email
                        template_id.send_mail(record.id, force_send=True, email_values={'email_to': email_to})
                        _logger.warning(f"!!! DEBUG: Email sent to {email_to} for record {record.id} !!!")

        _logger.warning("!!! DEBUG: set_confirm method finished successfully (state updated and emails sent). !!!")
        return True

    def set_done(self):
        self.write({'state': 'done'})

# # -*- coding: utf-8 -*-
# from odoo import models, fields, api
# from odoo.tools.translate import html_translate


# class UserNotification(models.Model):
#     _name = 'user.update.notification'
#     _description = 'user'

#     user = fields.Many2one('res.users', string="User")
#     useraction = fields.Selection([('new', 'New'), ('closed', 'closed')], default="new")
#     notification_id = fields.Many2one('new.update.notification', string="Notification", ondelete='cascade')


# class NewNotification(models.Model):
#     _name = 'new.update.notification'
#     _description = 'name'

#     name = fields.Char(string="Name")
#     description = fields.Html(string="Description", sanitize_attributes=False, translate=html_translate, sanitize_form=False)
#     state = fields.Selection([('new', 'Draft'), ('confirm', 'Active'), ('done', 'Close')], string="State", default='new')
#     user_notification_ids = fields.One2many('user.update.notification', 'notification_id', string="User Notification")

#     def set_draft(self):
#         self.state = 'new'

#     def set_confirm(self):
#         self.state = 'confirm'

#     def set_done(self):
#         self.state = 'done'

#     def action_open_wizard(self):
#         datas = {}
#         datas['popmodal'] = self.env['ir.ui.view']._render_template("mtech_new_notification.notication_popup_info", {
#             'newnoti': self
#         })
#         return datas

#     @api.model
#     def get_users_notify_datas(self):
#         recs = self.env['new.update.notification'].search([('state', '=', 'confirm')])
#         user_notification_ids = recs.mapped('user_notification_ids')
#         userids = user_notification_ids.filtered(lambda x: x.user == self.env.user)
#         recs = userids.mapped('notification_id')
#         recs_search_datas = recs.read(['name'])
#         counters = len(recs)
#         return {'notifydatas': recs_search_datas, 'notifycounter': counters}
