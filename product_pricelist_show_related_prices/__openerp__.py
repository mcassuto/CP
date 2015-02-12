# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Marc Cassuto <marc.cassuto@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': "Show list price and cost price in pricelist",
    'summary': "Show list price and cost price in pricelist",
    'version': "1.0",
    'depends': ["product"],
    'author': "Marc Cassuto <marc.cassuto@gmail.com>",
    'category': "Sales Management",
    'description': """
Show list price and cost price in pricelist
===========================================

When creating a pricelist, it can be usefull to have as a reference
the current cost of the product and the default sale price.

This module add this information on both the tree and form views of
the product_pricelist_iten object (visible from the pricelist versions).

Contributors
------------
* Marc Cassuto (marc.cassuto@gmail.com)
    """,
    "data": [
        'product_pricelist_item_view.xml'
    ],
    'update_xml': [],
    'demo_xml': [],
    'installable': True,
    'active': False,
    #    'certificate': '',
}
