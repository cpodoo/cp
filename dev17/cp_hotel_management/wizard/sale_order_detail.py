# -*- coding: utf-8 -*-

import json
import io
import pytz 
from datetime import datetime, time 
from odoo import fields, models, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import date_utils, DEFAULT_SERVER_DATETIME_FORMAT 

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    xlsxwriter = None

class SaleOrderWizard(models.TransientModel):
    _name = "sale.order.detail"
    _description = "Room Booking Details"

    checkin = fields.Date(help="Filter Start Date (Check-in)", string="Check In")
    checkout = fields.Date(help="Filter End Date (Check-out)", string="Check Out")

    def _get_filter_utc_range(self):
       
        user_tz_name = self.env.user.tz or 'UTC'
        user_tz = pytz.timezone(user_tz_name)
        utc = pytz.utc

        start_utc = None
        end_utc = None

        if self.checkin:
            start_naive = datetime.combine(self.checkin, time.min)
            start_local = user_tz.localize(start_naive, is_dst=None)
            start_utc = start_local.astimezone(utc)

        if self.checkout:
            end_naive = datetime.combine(self.checkout, time.max)
            end_local = user_tz.localize(end_naive, is_dst=None)
            end_utc = end_local.astimezone(utc)

        if self.checkin and not self.checkout:
            end_utc = start_utc.replace(hour=23, minute=59, second=59) 
        if not self.checkin and self.checkout:
             start_utc = end_utc.replace(hour=0, minute=0, second=0) 
        return start_utc, end_utc

    def generate_data(self):
        
        line_domain = []
        processed_bookings = {} 

        if not self.checkin or not self.checkout:
            raise UserError(_("Please select both Check In and Check Out dates for filtering."))
        if self.checkin > self.checkout:
            raise ValidationError(_("Filter Check-in date cannot be after Check-out date."))

        user_tz_name = self.env.user.tz or 'UTC'
        try:
            user_tz = pytz.timezone(user_tz_name)
        except pytz.UnknownTimeZoneError:
            user_tz = pytz.utc
        utc = pytz.utc

        checkin_day_start_utc = None
        try:
            start_naive = datetime.combine(self.checkin, time.min)
            start_local = user_tz.localize(start_naive, is_dst=None)
            checkin_day_start_utc = start_local.astimezone(utc)
        except Exception as e:
            print(f"Error calculating checkin start UTC: {e}")
            raise UserError(_("Could not process the Check In date."))

        checkout_day_start_utc = None
        try:
            checkout_start_naive = datetime.combine(self.checkout, time.min)
            checkout_start_local = user_tz.localize(checkout_start_naive, is_dst=None)
            checkout_day_start_utc = checkout_start_local.astimezone(utc)
        except Exception as e:
            print(f"Error calculating checkout start UTC: {e}")
            raise UserError(_("Could not process the Check Out date."))

        checkout_day_end_utc = None
        try:
            checkout_end_naive = datetime.combine(self.checkout, time.max)
            checkout_end_local = user_tz.localize(checkout_end_naive, is_dst=None)
            checkout_day_end_utc = checkout_end_local.astimezone(utc)
        except Exception as e:
             print(f"Error calculating checkout end UTC: {e}")
             raise UserError(_("Could not process the Check Out date."))
     
        if checkin_day_start_utc:
            line_domain.append(('checkin_date', '>=', checkin_day_start_utc))
        if checkout_day_start_utc:
            line_domain.append(('checkout_date', '>=', checkout_day_start_utc))
        if checkout_day_end_utc:
            line_domain.append(('checkout_date', '<=', checkout_day_end_utc))
        
        booking_lines = self.env['room.booking.line'].search(line_domain)

        for line in booking_lines:
            booking = line.booking_id
            if not booking or booking.id in processed_bookings:
                continue

            booking_data = booking.read([
                'partner_id', 'name', 'date_order', 'amount_total'
            ])
            if not booking_data: continue
            b_data = booking_data[0]

            partner_name = b_data.get('partner_id')[1] if b_data.get('partner_id') else 'N/A'
            order_date_dt = b_data.get('date_order') # Using date_order
            order_date_str = fields.Datetime.to_string(order_date_dt) if order_date_dt else ''

            line_checkin_dt = line.checkin_date
            line_checkout_dt = line.checkout_date
            line_checkin_str = fields.Datetime.to_string(line_checkin_dt) if line_checkin_dt else ''
            line_checkout_str = fields.Datetime.to_string(line_checkout_dt) if line_checkout_dt else ''

            rec_data = {
                'partner_id': partner_name,
                'name': b_data.get('name', ''),
                'date_order': order_date_str, 
                'amount_total': b_data.get('amount_total', 0.0),
                'checkin_date': line_checkin_str, 
                'checkout_date': line_checkout_str,
            }
            processed_bookings[booking.id] = rec_data

        return list(processed_bookings.values())
    def action_sale_order_pdf(self):
        booking_data = self.generate_data()
        if not booking_data:
            raise UserError(_("No booking records found matching the filter criteria."))
        data = {'booking': booking_data}
        return self.env.ref('cp_hotel_management.action_report_sale_order').report_action(self, data=data)

    def action_sale_order_excel(self):
        if not xlsxwriter:
            raise UserError(_("The 'xlsxwriter' library is not installed. Please install it (`pip3 install xlsxwriter`)."))
        booking_data = self.generate_data()
        if not booking_data:
            raise UserError(_("No booking records found matching the filter criteria."))
        data = {'booking': booking_data}
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'sale.order.detail',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Sale Order Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'font_size': '12px', 'bold': True, 'align': 'center', 'border': True})
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px', 'border': True})
        body = workbook.add_format({'align': 'left', 'text_wrap': True, 'border': True})
        datetime_format = workbook.add_format({'align': 'left', 'text_wrap': True, 'border': True, 'num_format': 'yyyy-mm-dd hh:mm:ss'})
        amount_format = workbook.add_format({'align': 'right', 'text_wrap': True, 'border': True, 'num_format': '#,##0.00'})

        sheet.merge_range('A1:F1', 'Sale Order', head) 
        sheet.set_column('A:A', 8)  
        sheet.set_column('B:B', 25) 
        sheet.set_column('C:D', 20) 
        sheet.set_column('E:E', 20) 
        sheet.set_column('F:F', 15) 

        sheet.set_row(0, 30)
        sheet.set_row(1, 20)

        sheet.write('A2', 'Sl No.', cell_format)
        sheet.write('B2', 'Guest Name', cell_format)
        sheet.write('C2', 'Check In Date', cell_format) 
        sheet.write('D2', 'Check Out Date', cell_format)   
        sheet.write('E2', 'Reference No.', cell_format)    
        sheet.write('F2', 'Total Amount', cell_format)    

        row = 2
        column = 0
        value = 1
        user_tz_name = self.env.user.tz or 'UTC'
        try:
            user_tz = pytz.timezone(user_tz_name)
        except pytz.UnknownTimeZoneError:
            user_tz = pytz.utc
        utc = pytz.utc

        for i in data.get('booking', []):
            def get_local_naive(utc_datetime_str):
                if not utc_datetime_str:
                    return None
                try:
                    dt_utc = fields.Datetime.from_string(utc_datetime_str)
                    dt_local = dt_utc.replace(tzinfo=utc).astimezone(user_tz)
                    return dt_local.replace(tzinfo=None)
                except Exception:
                    return None

            sheet.write(row, column + 0, value, body)
            sheet.write(row, column + 1, i.get('partner_id', ''), body) 

            checkin_naive = get_local_naive(i.get('date_order'))
            sheet.write(row, column + 2, checkin_naive, datetime_format)

            checkout_naive = get_local_naive(i.get('date_order'))
            sheet.write(row, column + 3, checkout_naive, datetime_format)

            sheet.write(row, column + 4, i.get('name', ''), body)

            sheet.write(row, column + 5, i.get('amount_total', 0.0), amount_format)

            row += 1
            value += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()