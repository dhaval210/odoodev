# -*- coding: utf-8 -*-

from odoo.addons.base.models.ir_qweb_fields import FloatConverter


def record_to_html(self, record, field_name, options):
    if 'precision' not in options and 'decimal_precision' not in options:
        if record._fields[field_name].get_description(self.env).get('digits'):
            _, precision = record._fields[field_name].get_description(self.env)['digits']
        else:
             _, precision = None, None
        options = dict(options, precision=precision)
    return super(FloatConverter, self).record_to_html(
        record, field_name, options)


FloatConverter.record_to_html = record_to_html