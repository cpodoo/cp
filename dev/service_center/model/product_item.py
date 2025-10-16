from odoo import fields,models,api

class ProductItem(models.Model):
    _name="product.item"
    _description="Product"
    # _name_search='brand_id'

    name=fields.Char(string="Name",required=True)
    description=fields.Char(string='Description')
    brand_id=fields.Many2one('brand.brand',string="Brand",required=True)
    image=fields.Image(string="Image",help="Select image")

    service_count = fields.Integer(string="Servies", compute='compute_service', default=0)

    def compute_service(self):
        for record in self:
            record.service_count = self.env['service.request.line'].search_count([('item_id', '=', self.id)])

    def action_get_service(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'servies',
            # 'view_type': 'from',
            'view_mode': 'form',
            'res_model': 'service.request',
            'domain': [('request_line.item_id', '=', self.id)],
            'context':{'default_customer_name':self.name},
            'target':'new'
        }

    def _name_search(self,name,args=None,operator='ilike',limit=100):
        args.append(('|', ('name', operator, name), ('brand_id.name', operator, name)))

        return self.search(args)
