# -*- coding: utf-8 -*-

try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.http import request
from odoo import http
from odoo.http import content_disposition
import zipfile
import ast

class Binary(http.Controller):
    @http.route('/web/binary/download_mo_zip', type='http', auth="public")
    def download_mo_zip(self, attachments, mo_type_code=False, **kw):
        attachments = ast.literal_eval(attachments)
        attachment_ids = request.env['ir.attachment'].search([('id', 'in', attachments)])
        file_dict = {}
        for attachment_id in attachment_ids:
            file_store = attachment_id.store_fname
            if file_store:
                file_name = attachment_id.name
                file_path = attachment_id._full_path(file_store)
                file_dict["%s:%s" % (file_store, file_name)] = dict(path=file_path, name=file_name)
        if file_dict:
            zip_initial = ''
            if mo_type_code:
                zip_initial = mo_type_code
            zip_filename = (zip_initial + '_' if zip_initial else '') + ','.join([y.split('.')[0].split('/')[-1] for y in [x['name'] for x in file_dict.values()]])
        else:
            zip_filename = "compressed_documents_" + datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        zip_filename = "%s.zip" % zip_filename
        bitIO = BytesIO()
        zip_file = zipfile.ZipFile(bitIO, "w", zipfile.ZIP_DEFLATED)
        for file_info in file_dict.values():
            zip_file.write(file_info["path"], file_info["name"].replace('/', '_'))
        zip_file.close()
        return request.make_response(bitIO.getvalue(),
                                     headers=[('Content-Type', 'application/x-zip-compressed'),
                                              ('Content-Disposition', content_disposition(zip_filename))])
