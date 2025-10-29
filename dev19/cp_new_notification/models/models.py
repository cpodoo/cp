# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import html_translate
from odoo.exceptions import UserError

class UserNotification(models.Model):
    _name = 'user.update.notification'
    _description = 'User Notification'

    user = fields.Many2one('res.users', string="User", required=True)
    useraction = fields.Selection([('new', 'New'), ('closed', 'Closed')], default="new")
    notification_id = fields.Many2one('new.update.notification', string="Notification", ondelete='cascade', required=True)


class NewNotification(models.Model):
    _name = 'new.update.notification'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Update Notification'

    name = fields.Char(string="Name", required=True)
    description = fields.Html(
        string="Description",
        sanitize_attributes=False,
        translate=html_translate,
        sanitize_form=False
    )
    state = fields.Selection([
        ('new', 'Draft'),
        ('confirm', 'Active'),
        ('done', 'Close')
    ], string="State", default='new', tracking=True)

    user_notification_ids = fields.One2many(
        'user.update.notification',
        'notification_id',
        string="User Notification"
    )

    def set_draft(self):
        for rec in self:
            rec.state = 'new'

    def set_done(self):
        for rec in self:
            rec.state = 'done'

    def set_confirm(self):
        template = self.env.ref('cp_new_notification.mail_template_notify_user', raise_if_not_found=False)

        if not template:
           
            raise UserError(('Mail template "cp_new_notification.mail_template_notify_user" not found. Cannot confirm notification.'))
         
        for record in self:
            record.state = 'confirm' 

            if not record.user_notification_ids:
                continue 
            for user_notif in record.user_notification_ids:
                user = user_notif.user
                partner = user.partner_id if user else None
                email_address = partner.email if partner else None
                if user and partner and email_address:
                    try:
                        template.send_mail(record.id, force_send=True, email_values={
                            'email_to': email_address,
                            'recipient_ids': [(6, 0, [partner.id])]
                        })
                    except Exception as e:
                        pass 

    def action_open_wizard(self):
        self.ensure_one()
        datas = {
            'popmodal': self.env['ir.ui.view']._render_template(
                "cp_new_notification.notication_popup_info",
                {'newnoti': self}
            )
        }
        return datas

    @api.model
    def get_users_notify_datas(self):
        user_notifications = self.env['user.update.notification'].search([
            ('user', '=', self.env.user.id),
            ('notification_id.state', '=', 'confirm')
        ])
        active_notifications = user_notifications.mapped('notification_id')
        notification_data = active_notifications.read(['name', 'description'])
        count = len(notification_data)
        return {'notifydatas': notification_data, 'notifycounter': count}
