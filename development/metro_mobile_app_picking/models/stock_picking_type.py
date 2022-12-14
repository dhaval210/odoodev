# Copyright (C) 2019-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'
    
    hightlight_picking = fields.Boolean(
        string='Move Packages to Locations',
        default=False)

    mobile_available = fields.Boolean(
        string='Available on Mobile',
        help="Check this box if you want to make this picking type visible"
        " on the Mobile App")

    mobile_backorder_create = fields.Boolean(
        string='Create Backorder', default=True,
        help="Check this box if you want that confirming a picking on mobile"
        " app generate a backorder by default.")

    mobile_product_field_ids = fields.Many2many(
        string='Product Fields', comodel_name='ir.model.fields',
        domain=[('model', 'in', ['product.product'])])
