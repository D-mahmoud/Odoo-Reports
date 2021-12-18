from odoo import models, fields, api



class request(models.Model):
    _name = 'dalia.request'
    _description = 'dalia.request'
    _order = 'sale_order_id desc'
    # sale_order_id = fields.Char(string="Sales order ID", readonly=True, help="Write your name")
    # customer_id = fields.Many2one(string='Customer', comodel_name='res.partner', ondelete='restrict', index=True)
    phone = fields.Char(string="Phone", required=False, help="Write your phone")
    date = fields.Datetime(string='Request Date', required=False, default=fields.Datetime.now, )
    # product_id = fields.Many2one(string='Product', comodel_name='product.product', ondelete='restrict')
    # route = fields.Selection(string='Destination', required=True, selection=[('5', 'Buy'), ('6', 'Manufactury')])
    # bom_id = fields.Many2one(string='Bill of material', comodel_name='mrp.bom', ondelete='restrict')
    value = fields.Float(string='Estimated Value')
    qty = fields.Float(string='Quantity', required=False)
    # uom_id = fields.Many2one(stany2onring='Unit Of Measure', comodel_name='uom.uom', ondelete='restrict', )
   