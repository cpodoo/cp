# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Disease(models.Model):
    _name = 'disease'
    _description = "Disease"

    disease_name=fields.Char("Disease Name")
    code=fields.Char()
    disease_category=fields.Many2one("disease.category")


class DiseaseCategory(models.Model):
    _name = 'disease.category'
    _description = "Disease Category"

    category_name=fields.Char("Category")