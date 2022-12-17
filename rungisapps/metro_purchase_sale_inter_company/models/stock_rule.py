# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import UserError


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _make_po_get_domain(self, values, partner):
        domain = super(StockRule, self)._make_po_get_domain(values, partner)
        so_id = self.env['sale.order.line'].browse(values.get('sale_line_id'))
        po = self.env['purchase.order'].sudo().search([('origin', '=', so_id.order_id.name)])
        if not po:
            domain += (
                ('id', '=', '0'),
            )
        else:
            domain += (
                        ('id', 'in', tuple(po.ids)),
                    )
        return domain

