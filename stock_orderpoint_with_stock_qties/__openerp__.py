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
    'name': "Stock Orrderpoint With Stock Quantities",
    'summary': 'Add the quantity on hand and forecasted quantity in the \
               orderpoint tree view',
    'version': "1.0",
    'depends': [
        'procurement',
        'product'
    ],
    'author': "Marc Cassuto",
    'category': "Stock",
    'description': """
Add the stock in hand and forecast stock in the orderpoint tree view.
=====================================================================

This helps the production manager to adjust his min/max rules.

Contributors
------------
* Marc Cassuto (marc.cassuto@gmail.com)
    """,
    'data': [
        'stock_warehouse_orderpoint_view.xml',
    ],
    'update_xml': [],
    'demo_xml': [],
    'installable': True,
    'active': False,
    #    'certificate': '',
}
