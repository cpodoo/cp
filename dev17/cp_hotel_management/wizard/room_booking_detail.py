# -*- coding: utf-8 -*-

import json
import io
from datetime import timedelta, datetime, time
from odoo import fields, models, _
from odoo.exceptions import ValidationError, UserError 
from odoo.tools import date_utils, misc
import pytz

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    xlsxwriter = None

class RoomBookingWizard(models.TransientModel):
    _name = "room.booking.detail"
    _description = "Room Booking Details"

    checkin = fields.Date(help="Choose the Checkin Date", string="Checkin")
    checkout = fields.Date(help="Choose the Checkout Date", string="Checkout")
    room = fields.Many2one("hotel.room", string="Room", help="Choose The Room")

    def _get_wizard_range_utc(self):
        """Converts wizard dates to a UTC datetime range."""
        start_utc = None
        end_utc = None
        user_tz_name = self.env.user.tz or self.env.context.get('tz') or 'UTC'
        user_tz = pytz.timezone(user_tz_name)
        utc = pytz.utc

        try:
            if self.checkin:
                start_dt_naive = datetime.combine(self.checkin, time.min) 
                start_dt_aware = user_tz.localize(start_dt_naive, is_dst=None)
                start_utc = start_dt_aware.astimezone(utc)

            if self.checkout:
                end_dt_naive = datetime.combine(self.checkout, time.max) 
                end_dt_aware = user_tz.localize(end_dt_naive, is_dst=None)
                end_utc = end_dt_aware.astimezone(utc)

        except Exception as e:
            pass
        return start_utc, end_utc

    def action_room_booking_pdf(self):
        """Button action_room_booking_pdf function"""
        report_data = self.generate_data()
        data = {"booking": report_data}
        return self.env.ref(
            "cp_hotel_management.action_report_room_booking"
        ).report_action(self, data=data)

    def action_room_booking_excel(self):
        """Button action for creating Room Booking Excel report"""
        if not xlsxwriter:
             raise UserError(_("The library 'xlsxwriter' is required for Excel reports, but it's not installed. Please contact your administrator."))
        report_data = self.generate_data()
        data = {"booking": report_data}
        return {
            "type": "ir.actions.report",
            "data": {
                "model": "room.booking.detail",
                "options": json.dumps(data, default=date_utils.json_default),
                "output_format": "xlsx",
                "report_name": "Room Booking Report.xlsx",
            },
            "report_type": "xlsx",
        }

    def generate_data(self):
        room_line_domain = []
        room_list = []
        user_tz = pytz.timezone(self.env.user.tz or 'UTC')

        if self.checkin and self.checkout and self.checkin > self.checkout:
            raise ValidationError(_("Check-in date should be less than Check-out date"))

        if self.checkin and self.checkout and self.checkin == self.checkout:
            single_day_start_utc, single_day_end_utc = self._get_wizard_range_utc()

            if single_day_start_utc and single_day_end_utc:
                room_line_domain.append(('checkin_date', '>=', single_day_start_utc))
                room_line_domain.append(('checkin_date', '<=', single_day_end_utc))
                room_line_domain.append(('checkout_date', '>=', single_day_start_utc))
                room_line_domain.append(('checkout_date', '<=', single_day_end_utc))
            else:
                 pass 

        elif self.checkout: 
            checkout_day_start_utc = None
            checkout_day_end_utc = None
            utc = pytz.utc
            try:
                checkout_start_naive = datetime.combine(self.checkout, time.min)
                checkout_end_naive = datetime.combine(self.checkout, time.max)
                checkout_day_start_utc = user_tz.localize(checkout_start_naive, is_dst=None).astimezone(utc)
                checkout_day_end_utc = user_tz.localize(checkout_end_naive, is_dst=None).astimezone(utc)
            except Exception:
                pass 

            if checkout_day_start_utc and checkout_day_end_utc:
                room_line_domain.append(('checkout_date', '>=', checkout_day_start_utc))
                room_line_domain.append(('checkout_date', '<=', checkout_day_end_utc))

        if self.room:
            room_line_domain.append(('room_id', '=', self.room.id))


        booking_lines_data = self.env["room.booking.line"].search_read(
            room_line_domain,
            fields=['id', 'booking_id', 'room_id', 'checkin_date', 'checkout_date'],
            order='checkout_date asc' 
        )

        for line_data in booking_lines_data:
            booking_id = line_data['booking_id'][0] if line_data.get('booking_id') else None
            room_name = line_data['room_id'][1] if line_data.get('room_id') else ''

            booking_rec = self.env['room.booking'].browse(booking_id)
            partner_name = booking_rec.partner_id.name if booking_rec.partner_id else ''
            booking_name = booking_rec.name

            checkin_dt = line_data['checkin_date']
            checkout_dt = line_data['checkout_date']

            checkin_dt_naive = None
            checkout_dt_naive = None
            try:
                if isinstance(checkin_dt, datetime):
                    checkin_dt_naive = checkin_dt.astimezone(user_tz).replace(tzinfo=None)
                if isinstance(checkout_dt, datetime):
                    checkout_dt_naive = checkout_dt.astimezone(user_tz).replace(tzinfo=None)
            except Exception:
                continue

            rec_data = {
                'partner_id': partner_name,
                'name': booking_name,
                'room': room_name,
                'checkin_date': checkin_dt,
                'checkout_date': checkout_dt,
                'checkin_date_naive': checkin_dt_naive,
                'checkout_date_naive': checkout_dt_naive,
            }
            room_list.append(rec_data)

        return room_list


    def get_xlsx_report(self, data, response):
        """Organizing xlsx report"""
        if not xlsxwriter:
             raise UserError(_("The library 'xlsxwriter' is required for Excel reports, but it's not installed. Please contact your administrator."))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True, 'remove_timezone': True})
        sheet = workbook.add_worksheet("Room Booking Report")
        cell_format = workbook.add_format({"font_size": "11px", "bold": True, "align": "center", "border": 1, "valign": "vcenter"})
        head = workbook.add_format({"align": "center", "bold": True, "font_size": "16px", "border": 1, "valign": "vcenter"})
        body = workbook.add_format({"font_size": "10px", "align": "left", "border": 1, "valign": "top"})
        datetime_format_excel = workbook.add_format({'font_size': '10px', 'align': 'left', 'border': 1, 'valign': 'top', 'num_format': 'yyyy-mm-dd hh:mm'})

        sheet.merge_range("A1:F1", "Room Booking Report", head)
        sheet.set_column("A:A", 5); sheet.set_column("B:B", 25); sheet.set_column("C:C", 15); sheet.set_column("D:E", 18); sheet.set_column("F:F", 20)
        sheet.set_row(0, 25); sheet.set_row(1, 18)
        sheet.write("A2", "Sl No.", cell_format); sheet.write("B2", "Guest Name", cell_format); sheet.write("C2", "Room No.", cell_format)
        sheet.write("D2", "Check In", cell_format); sheet.write("E2", "Check Out", cell_format); sheet.write("F2", "Reference No.", cell_format)

        row = 2
        bookings_data = data.get("booking", [])

        if not bookings_data:
             sheet.merge_range(row, 0, row, 5, "No booking details found for the selected criteria.", body)
        else:
            for idx, i in enumerate(bookings_data, start=1):
                sheet.write(row, 0, idx, body)
                sheet.write(row, 1, i.get("partner_id", ""), body)
                sheet.write(row, 2, i.get("room", ""), body)

                checkin_dt_to_write = i.get("checkin_date_naive")
                checkout_dt_to_write = i.get("checkout_date_naive")

                if isinstance(checkin_dt_to_write, datetime):
                    try:
                        sheet.write_datetime(row, 3, checkin_dt_to_write, datetime_format_excel)
                    except Exception as e_write:
                        sheet.write(row, 3, 'Error', body)
                elif checkin_dt_to_write:
                    sheet.write(row, 3, str(checkin_dt_to_write), body)
                else:
                    sheet.write(row, 3, '', body)

                if isinstance(checkout_dt_to_write, datetime):
                     try:
                        sheet.write_datetime(row, 4, checkout_dt_to_write, datetime_format_excel)
                     except Exception as e_write:
                        sheet.write(row, 4, 'Error', body)
                elif checkout_dt_to_write:
                    sheet.write(row, 4, str(checkout_dt_to_write), body)
                else:
                    sheet.write(row, 4, '', body)

                sheet.write(row, 5, i.get("name", ""), body)
                row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

# # -*- coding: utf-8 -*-

# import json
# import io
# from odoo import fields, models, _
# from odoo.exceptions import ValidationError
# from odoo.tools import date_utils

# try:
#     from odoo.tools.misc import xlsxwriter
# except ImportError:
#     import xlsxwriter


# class RoomBookingWizard(models.TransientModel):
#     """Pdf Report for room Booking"""

#     _name = "room.booking.detail"
#     _description = "Room Booking Details"

#     checkin = fields.Date(help="Choose the Checkin Date", string="Checkin")
#     checkout = fields.Date(help="Choose the Checkout Date", string="Checkout")
#     room = fields.Many2one("hotel.room", string="Room", help="Choose The Room")

#     def action_room_booking_pdf(self):
#         """Button action_room_booking_pdf function"""
#         data = {
#             "booking": self.generate_data(),
#         }
#         return self.env.ref(
#             "cp_hotel_management.action_report_room_booking"
#         ).report_action(self, data=data)

#     def action_room_booking_excel(self):
#         """Button action for creating Room Booking Excel report"""
#         data = {
#             "booking": self.generate_data(),
#         }
#         return {
#             "type": "ir.actions.report",
#             "data": {
#                 "model": "room.booking.detail",
#                 "options": json.dumps(data, default=date_utils.json_default),
#                 "output_format": "xlsx",
#                 "report_name": "Excel Report",
#             },
#             "report_type": "xlsx",
#         }

#     def generate_data(self):
#         """Generate data to be printed in the report"""
#         domain = []
#         room_list = []
#         if self.checkin and self.checkout:
#             if self.checkin > self.checkout:
#                 raise ValidationError(
#                     _("Check-in date should be less than Check-out date")
#                 )
#         if self.checkin:
#             domain.append(
#                 ("checkin_date", ">=", self.checkin),
#             )
#         if self.checkout:
#             domain.append(
#                 ("checkout_date", "<=", self.checkout),
#             )
#         room_booking = self.env["room.booking"].search_read(
#             domain=domain,
#             fields=["partner_id", "name", "checkin_date", "checkout_date"],
#         )
#         for rec in room_booking:
#             rooms = (
#                 self.env["room.booking"]
#                 .browse(rec["id"])
#                 .room_line_ids.room_id.mapped("name")
#             )
#             rec["partner_id"] = rec["partner_id"][1]
#             for room in rooms:
#                 if self.room:
#                     if self.room.name == room:
#                         rec["room"] = room
#                         room_list.append(rec)
#                 else:
#                     rec_copy = rec.copy()
#                     rec_copy["room"] = room
#                     room_list.append(rec_copy)

#         return room_list

#     def get_xlsx_report(self, data, response):
#         """Organizing xlsx report"""
#         output = io.BytesIO()
#         workbook = xlsxwriter.Workbook(output, {"in_memory": True})
#         sheet = workbook.add_worksheet()
#         cell_format = workbook.add_format(
#             {"font_size": "14px", "bold": True, "align": "center", "border": True}
#         )
#         head = workbook.add_format(
#             {"align": "center", "bold": True, "font_size": "23px", "border": True}
#         )
#         body = workbook.add_format({"align": "left", "text_wrap": True, "border": True})
#         sheet.merge_range("A1:F1", "Room Booking", head)
#         sheet.set_column("A2:F2", 18)
#         sheet.set_row(0, 30)
#         sheet.set_row(1, 20)
#         sheet.write("A2", "Sl No.", cell_format)
#         sheet.write("B2", "Guest Name", cell_format)
#         sheet.write("C2", "Room No.", cell_format)
#         sheet.write("D2", "Check In", cell_format)
#         sheet.write("E2", "Check Out", cell_format)
#         sheet.write("F2", "Reference No.", cell_format)
#         row = 2
#         column = 0
#         value = 1
#         for i in data["booking"]:
#             sheet.write(row, column, value, body)
#             sheet.write(row, column + 1, i["partner_id"], body)
#             sheet.write(row, column + 2, i["room"], body)
#             sheet.write(row, column + 3, i["checkin_date"], body)
#             sheet.write(row, column + 4, i["checkout_date"], body)
#             sheet.write(row, column + 5, i["name"], body)
#             row = row + 1
#             value = value + 1
#         workbook.close()
#         output.seek(0)
#         response.stream.write(output.read())
#         output.close()
