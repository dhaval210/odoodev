# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Avinash Nk(<https://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Expiry Date Warning Fix',
    'category': 'Metro',
    'summary': """Generates Warning for Expired Products, When it sells. MODIFIED TO BASE ON EXPIRY DATE """,
    'description': """ Added fix on 19th March 2019 by Ankita Padhi, MWM IT (ankita.padhi@metro-wholesale.com) to eleminate the Loading time error of adding certain products to sale order. MODIFIED TO BASE ON EXPIRY DATE. v0.3: PATCHED FOR PERFORMANCE BY ODOO SA""",
    'version': '12.0.2',
    'author': 'Cybrosys Techno Solutions, Odoo s.a., Metro',
    "category": "Sales",
    "depends": ["sale_management", "product_expiry"],
    'installable': True,
    'application': False,
}
