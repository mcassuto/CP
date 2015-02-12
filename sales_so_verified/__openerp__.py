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
    'name': "Set a flag verified on sales orders",
    'summary': "Set a flag verified on sales orders",
    'version': "1.0",
    'depends': ["sale"],
    'author': "Marc Cassuto <marc.cassuto@gmail.com>",
    'category': "Sales",
    'description': """

This module allows to flag sales orders as 'verified'
=====================================================

Introduction
------------

Sometimes, a sales order can remain in state "Sale Order" and never being
marked as 'done'. There is various explanation for that...

So in some case, it can be useful to flag these sales orders in order to
filter them out (or in).

What this module does ?
-----------------------

It add a new tab 'Verification' in the sale order form, visible only by the
sales managers.

This tab contains to field :

* a boolean to actually flag the sale order;
* a text field to explain the reason of the flag.

Any modification to theses fields will trigger a note in the tracker.

Finally, 2 new filters 'Verified' and 'Not Verified' are added to the
sale order search view.

Contributors
------------
* Marc Cassuto (marc.cassuto@gmail.com)
    """,
    "data": [
        'sale_order_view.xml'
    ],
    'update_xml': [],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
