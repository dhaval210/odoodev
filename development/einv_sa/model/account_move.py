#!/usr/bin/python
# -*- coding: utf-8 -*-
import base64

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning


class AccountMove(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"
    einv_amount_sale_total = fields.Monetary(string="Amount sale total", compute="_compute_total", store='True',
                                             help="")
    einv_amount_discount_total = fields.Monetary(string="Amount discount total", compute="_compute_total", store='True',
                                                 help="")
    einv_amount_tax_total = fields.Monetary(string="Amount tax total", compute="_compute_total", store='True', help="")

    # amount_invoiced = fields.Float(string="Amount tax total", help="")
    # qrcode = fields.Char(string="QR", help="")
    # region odoo standard -------------------------
    einv_sa_delivery_date = fields.Date(string='Delivery Date', default=fields.Date.context_today, copy=False)
    einv_sa_show_delivery_date = fields.Boolean(compute='_compute_show_delivery_date')
    einv_sa_qr_code_str = fields.Char(string='Zatka QR Code', compute='_compute_qr_code_str')
    einv_sa_confirmation_datetime = fields.Datetime(string='Confirmation Date', readonly=True, copy=False)
    country_code = fields.Char(related='company_id.country_id.code', readonly=True)

    @api.depends('country_code', 'type')
    def _compute_show_delivery_date(self):
        self.einv_sa_show_delivery_date = False
        for move in self:
            move.einv_sa_show_delivery_date = move.country_code == 'SA' and move.type in (
                'out_invoice', 'out_refund')

    @api.depends('amount_total', 'amount_untaxed', 'einv_sa_confirmation_datetime', 'company_id', 'company_id.vat')
    def _compute_qr_code_str(self):
        """ Generate the qr code for Saudi e-invoicing. Specs are available at the following link at page 23
        https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/20210528_ZATCA_Electronic_Invoice_Security_Features_Implementation_Standards_vShared.pdf
        https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/QRCodeCreation.pdf
        """

        def get_qr_encoding(tag, field):
            company_name_byte_array = field.encode('UTF-8')
            company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
            company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
            return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array

        for record in self:
            qr_code_str = ''
            if record.einv_sa_confirmation_datetime and record.company_id.vat:
                seller_name_enc = get_qr_encoding(1, record.company_id.display_name)
                company_vat_enc = get_qr_encoding(2, record.company_id.vat)
                time_sa = fields.Datetime.context_timestamp(self.with_context(tz='Asia/Riyadh'),
                                                            record.einv_sa_confirmation_datetime)
                timestamp_enc = get_qr_encoding(3, time_sa.isoformat())
                invoice_total_enc = get_qr_encoding(4, str(record.amount_total))
                total_vat_enc = get_qr_encoding(5, str(record.currency_id.round(
                    record.amount_total - record.amount_untaxed)))

                str_to_encode = seller_name_enc + company_vat_enc + timestamp_enc + invoice_total_enc + total_vat_enc
                qr_code_str = base64.b64encode(str_to_encode).decode('UTF-8')
            record.einv_sa_qr_code_str = qr_code_str

    def invoice_validate(self, soft=True):
        res = super().invoice_validate()
        for record in self:
            if record.country_code == 'SA' and record.type in ('out_invoice', 'out_refund'):
                if not record.einv_sa_show_delivery_date:
                    raise UserError(_('Delivery Date cannot be empty'))
                if record.einv_sa_delivery_date < record.date_invoice:
                    raise UserError(_('Delivery Date cannot be before Invoice Date'))
                self.write({
                    'einv_sa_confirmation_datetime': fields.Datetime.now()
                })
        return res

    # endregion
    @api.depends('invoice_line_ids', 'amount_total')
    def _compute_total(self):
        for r in self:
            r.einv_amount_sale_total = r.amount_untaxed + sum(line.einv_amount_discount for line in r.invoice_line_ids)
            r.einv_amount_discount_total = sum(line.einv_amount_discount for line in r.invoice_line_ids)
            r.einv_amount_tax_total = sum(line.einv_amount_tax for line in r.invoice_line_ids)

    def _compute_amount(self):
        res = super(AccountMove, self)._compute_amount()

        # do the things here
        return res




class AccountMoveLine(models.Model):
    _name = "account.invoice.line"
    _inherit = "account.invoice.line"
    einv_amount_discount = fields.Monetary(string="Amount discount", compute="_compute_amount_discount", store='True',
                                           help="")
    einv_amount_tax = fields.Monetary(string="Amount tax", compute="_compute_amount_tax", store='True', help="")

    @api.depends('discount', 'quantity', 'price_unit')
    def _compute_amount_discount(self):
        for r in self:
            r.einv_amount_discount = r.quantity * r.price_unit * (r.discount / 100)

    @api.depends('invoice_line_tax_ids', 'discount', 'quantity', 'price_unit')
    def _compute_amount_tax(self):
        for r in self:
            r.einv_amount_tax = sum(r.price_subtotal * (tax.amount / 100) for tax in r.invoice_line_tax_ids)
