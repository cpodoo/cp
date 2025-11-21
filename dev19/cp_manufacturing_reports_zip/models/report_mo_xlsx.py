# -*- coding: utf-8 -*-

from odoo import models
import io
import xlsxwriter
from odoo.exceptions import UserError

class ReportMOXlsx(models.AbstractModel):
    _name = 'report.cp_manufacturing_reports_zip.report_mo_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, manufacturing_orders):
        """
        Generate a single Excel report with multiple sheets, one for each Manufacturing Order.

        Args:
            workbook (xlsxwriter.Workbook): The Excel workbook object.
            data (dict): A dictionary of data (optional, can be used for filtering or passing context).
            manufacturing_orders (mrp.production recordset): The Manufacturing Orders to include in the report.
        """

        if not manufacturing_orders:
            raise UserError("No Manufacturing Orders selected for the report.")

        # Define cell formats here (outside the loop for efficiency)
        bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        border = workbook.add_format({'border': 1})

        # Iterate through the manufacturing orders and create a sheet for each
        for mo in manufacturing_orders:
            try:
                sheet = workbook.add_worksheet(mo.name[:31])  # Sheet name cannot exceed 31 characters
                sheet.set_column(0, 6, 20)  # Set column width

                # Header
                sheet.merge_range('A2:D3', f'Manufacturing Order - {mo.name}', bold)
                sheet.write('A5', 'Product', bold)
                sheet.write('B5', mo.product_id.display_name, border)
                sheet.write('A6', 'Quantity to Produce', bold)
                sheet.write('B6', mo.product_qty, border)
                sheet.write('A7', 'Scheduled Date', bold)
                sheet.write('B7', str(mo.date_start), border)
                sheet.write('A8', 'Component Status', bold)
                sheet.write('B8', mo.state, border)
                sheet.write('A10', 'Components', bold)
                sheet.write('A17', 'Work Orders', bold)

                # Table Header
                row = 11
                sheet.write(row, 0, 'Product', bold)
                sheet.write(row, 1, 'To Consume', bold)
                sheet.write(row, 2, 'Quantity', bold)
                sheet.write(row, 3, 'Consumed', bold)

                # Add Component Data
                row += 1
                for line in mo.move_raw_ids:
                    sheet.write(row, 0, line.product_id.display_name, border)
                    sheet.write(row, 1, line.product_uom_qty, border)
                    sheet.write(row, 2, line.quantity, border)
                    sheet.write(row, 3, line.picked, border)
                    row += 1

                # Table Header
                row = 18
                sheet.write(row, 0, 'Operation', bold)
                sheet.write(row, 1, 'Work Center', bold)
                sheet.write(row, 2, 'Product', bold)
                sheet.write(row, 3, 'Quantity To Be Produced', bold)
                sheet.write(row, 4, 'Expected Duration', bold)
                sheet.write(row, 5, 'Real Duration', bold)
                sheet.write(row, 6, 'status', bold)

                # Add Work Order Data
                row += 1
                for line in mo.workorder_ids:
                    sheet.write(row, 0, line.name, border)
                    sheet.write(row, 1, line.workcenter_id.name, border)
                    sheet.write(row, 2, line.product_id.display_name, border)
                    sheet.write(row, 3, line.qty_remaining, border)
                    sheet.write(row, 4, line.duration_expected, border)
                    sheet.write(row, 5, line.duration, border)
                    sheet.write(row, 6, line.state, border)
                    row += 1
            except Exception as e:
                # Handle exceptions for each MO and log error for user
                raise UserError(f"Error generating sheet for MO {mo.name}: {e}")
