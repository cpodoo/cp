# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError

class NotificationUpdate(http.Controller):

    @http.route('/check/new/notification', type='json', auth="user")
    def check_notification(self, **post):
        datas = {}
        try:
            user_obj = request.env.user
            # Ensure it's a logged-in internal user
            if not user_obj or user_obj.has_group('base.group_public'):
                return datas

            if request.session.get('cp_notification_shown_this_session'):
                return datas

            active_notifications = request.env['new.update.notification'].search([('state', '=', 'confirm')])
            if not active_notifications:
                return datas

            user_notification_recs = request.env['user.update.notification'].search([
                ('notification_id', 'in', active_notifications.ids),
                ('user', '=', user_obj.id),
                ('useraction', '=', 'new')
            ], limit=1)

            if user_notification_recs:
                notification_to_show = user_notification_recs.notification_id
                popup_html = request.env['ir.ui.view'].sudo()._render_template(
                    "cp_new_notification.notication_popup_info",
                    {'newnoti': notification_to_show}
                )
                datas['popmodal'] = popup_html
                datas['title'] = notification_to_show.name or "Notification"

                user_notification_recs.sudo().write({'useraction': 'closed'})
                request.session['cp_notification_shown_this_session'] = True

        except AccessError:
            return {}
        except Exception:
            return {}

        return datas
