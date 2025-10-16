from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class SubscriptionSubscription(models.Model):
    _name = 'subscription.subscription'
    _description = 'Subscription'

    @api.model
    def cron_delivery_reminder_mail_send(self):
        days = int(self.env["ir.config_parameter"].sudo().get_param("your_module.subscription_before_delivery_reminder_days", 3))
        if days >= 1:
            mail_date = fields.Date.context_today(self) + relativedelta(days=days)
            subscriptions_lines = self.env['subscription.line'].search([
                ('recurring_next_date', '=', mail_date),
                ('state', '=', 'in_progress')
            ])
            for subscription in subscriptions_lines.mapped('subscription_id'):
                email_context = self.env.context.copy()
                email_context.update({
                    'delivery_reminder_days': days,
                    'subscriptions_lines': [
                        {'product': line.product_id.name, 'qty': line.quantity}
                        for line in subscription.subscription_line_ids.filtered(lambda x: x in subscriptions_lines)
                    ],
                    'subscription': subscription,
                    'commitment_date': mail_date
                })
                template = self.env.ref('your_module.reminder_mail_for_delivery')
                template.with_context(email_context).send_mail(subscription.id)
