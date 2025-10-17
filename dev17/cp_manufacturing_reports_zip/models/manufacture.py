# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import UserError
import base64

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_mo_download_zip(self):
        attachment_ids = []
        for mo in self:
            mo_report = self.company_id.mo_report_zip
            if not mo_report:
                mo_report = self.env.ref('mrp.action_report_production_order')
            if mo_report:
                report_name = mo.name
                if mo_report.report_type in ['qweb-html', 'qweb-pdf']:
                    result, format = mo_report._render_qweb_pdf(report_ref=mo_report, res_ids=[mo.id])
                else:
                    res = mo_report.render(res_ids=[mo.id])
                    if not res:
                        raise UserError(_('Unsupported report type %s found.') % mo_report.report_type)
                    result, format = res
                result = base64.b64encode(result)
                ext = "." + format
                if not report_name.endswith(ext):
                    report_name += ext
                attachments = [(report_name, result)]
                Attachment = self.env['ir.attachment']
                for attach_fname, attach_datas in attachments:
                    data_attach = {
                        'name': attach_fname,
                        'datas': attach_datas,
                        'res_model': 'mrp.production',
                        'res_id': mo.id,
                        'type': 'binary',
                    }
                    attachment_ids.append(Attachment.create(data_attach).id)
        mo_type_code = [name.split('/')[0] + '_' + name.split('/')[1] for name in self.mapped('name')]
        mo_type_code_str = 'account_documents_'
        if len(set(mo_type_code)) == 1:
            mo_type_code_str = mo_type_code[0]
        else:
            mo_type_code = 'WH_MO'
        url = '/web/binary/download_mo_zip?attachments=%s&mo_type_code=%s' % (attachment_ids, mo_type_code_str)
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    def print_excel_report(self):
        """ Call the report action to generate Excel file """
        return self.env.ref('cp_manufacturing_reports_zip.action_mo_report_xlsx').report_action(self)

    def generate_mo_excel_report(self, active_ids):
        """Generate a single Excel report for all Manufacturing Orders from Action Menu"""
        manufacturing_orders = self.env['mrp.production'].browse(active_ids)
        if not manufacturing_orders:
            raise UserError(("No manufacturing orders found."))

        return self.env.ref('cp_manufacturing_reports_zip.action_mo_report_xlsx').report_action(manufacturing_orders)