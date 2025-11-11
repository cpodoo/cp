# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Attachments(models.Model):
    _name = 'attachments'
    _description = "Product Image"

    name = fields.Char("Name", default='Photo',tracking=True)
    sequence = fields.Integer(default=10, index=True,tracking=True)
    image_1920 = fields.Image(required=True,tracking=True)
    doctor_id = fields.Many2one('res.partner', "Doctor Id",tracking=True)
    post_operation_id = fields.Many2one('post.operation.wound', "Post-Op Id",tracking=True)