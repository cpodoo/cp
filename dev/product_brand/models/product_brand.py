from odoo import api, fields, models


class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brand'

    name = fields.Char(string="Name", help="Name of the brand")
    brand_image = fields.Binary(string="Image", help="Image of the brand")
    member_ids = fields.One2many('product.template', 'brand_id',
                                 string="Members",
                                 help="Products under the brand")
    product_count = fields.Char(string='Product Count',
                                compute='_compute_product_count', store=True,
                                help="Total number of products in the brand")

    stage = fields.Selection([
        ('new', 'New'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
    ], string="Stage", default='new', required=True)

    @api.depends('member_ids')
    def _compute_product_count(self):
        for record in self:
            record.product_count = len(record.member_ids)

    def action_approve(self):
        for rec in self:
            rec.stage = 'approved'

    def action_cancel(self):
        for rec in self:
            rec.stage = 'cancelled'
