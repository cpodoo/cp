# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import fields, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
# from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.osv import expression
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import werkzeug

class CustomerPortal(CustomerPortal):

    @http.route(['/dev_courier_track'], type='json', methods=['POST'], website=True, auth="public")
    def dev_track_courier_order(self, do_no, **kw):
        courier_id = request.env['dev.courier.request'].sudo().search([('name','=',do_no)],limit=1)
        status = False
        if courier_id:
            status = courier_id.state_id.name
            name = courier_id.name or ''
            sender_name = courier_id.sender_name
            receiver_name = courier_id.receiver_name
            delivery_date = courier_id.delivery_date
            if delivery_date:
                delivery_date = delivery_date.strftime("%d-%m-%Y")
            res = {
                'status':status or '',
                'name':name or '',
                'sender_name':sender_name or '',
                'receiver_name':receiver_name or '',
                'delivery_date':delivery_date,
            }
            return res
        else:
            return False
    
    @http.route(['/courier/tracking'], type='http', auth="public", website=True)
    def courier_tracking(self, **post):
        return request.render("dev_courier_management.courier_tracking_page")
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
            

