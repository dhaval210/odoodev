from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    last_purchase_price = fields.Float(
        string='Last Purchase Price', company_dependent=True, currency_id='currency_id')
    currency_id = fields.Many2one('res.currency', compute='compute_currency_id')

    def compute_currency_id(self):
        for rec in self:
            rec.currency_id = rec.env.user.company_id.id

    @api.multi
    def set_product_last_purchase(self, company_id=None):
        PurchaseOrderLine = self.env['purchase.order.line']
        for product in self:
            price_unit_uom = 0.0
            domain = [('product_id', '=', product.id),
                      ('state', 'in', ['purchase', 'done'])]
            if company_id:
                domain.append(('company_id', '=', company_id))
            lines = PurchaseOrderLine.search(domain).sorted(
                key=lambda l: l.order_id.date_order, reverse=True)

            if lines:
                # Get most recent Purchase Order Line
                last_line = lines[:1]
                # Compute Price Unit in the Product base UoM
                price_unit_uom = product.uom_id._compute_lpp_quantity(
                    last_line.price_unit, last_line.product_uom)
            product.with_context(force_company=company_id).write({
                "last_purchase_price": price_unit_uom,
            })
            # Set related product template values
            product.product_tmpl_id.set_product_template_last_purchase(price_unit_uom,company_id)
            return True

    def update_product_last_purchase(self, company_id=None):
        PurchaseOrderLine = self.env['purchase.order.line']
        products = self.search([('last_purchase_price', '=', 0), ('qty_available', '>', 0)])
        for product in products:
            price_unit_uom = 0.0
            domain = [('product_id', '=', product.id),
                      ('state', 'in', ['purchase', 'done'])]
            if company_id:
                domain.append(('company_id', '=', company_id))
            lines = PurchaseOrderLine.search(domain).sorted(
                key=lambda l: l.order_id.date_order, reverse=True)

            if lines:
                last_line = lines[:1]
                price_unit_uom = product.uom_id._compute_lpp_quantity(
                    last_line.price_unit, last_line.product_uom)
            product.write({
                "last_purchase_price": price_unit_uom,
            })
            product.product_tmpl_id.set_product_template_last_purchase(price_unit_uom)

    def update_lpp(self):
        self.update_product_last_purchase(1)
        self.update_product_last_purchase(4)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    last_purchase_price = fields.Float(
        string='Last Purchase Price', track_visibility='onchange', company_dependent=True)

    def set_product_template_last_purchase(self, price_unit,company_id=None):
        return self.with_context(force_company=company_id).write({
            "last_purchase_price": price_unit,
        })
