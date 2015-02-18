# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2010 - 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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
    'name': 'Product Margins in Invoices',
    'version': '0.1',
    'author': 'Marc Cassuto <marc.cassuto@gmail.com>',
    'license': 'AGPL-3',
    'category': 'Others',
    'summary': 'Product Margins in invoices based on list & standard prices',

    'description': """
Product Margins in Invoices
===========================

This module computes product's margin based on the invoice lines.

It adds a new report :

* Reporting \ Accounting \ Product Maring on Invoices

This report is showing the following columns :

* group: the main grouping column, by default the product
* Manuf. Cost: the 'Cost price' field from the product
* List Price: the 'List Price' field from the product
* Gross Margin on list price: calculated as List price - Cost price
* Gross Margin on list price (%): Gross Margin on list price rate
* Avg. Invoiced Price: Average price in customer invoices
* Gross Margin on invoices: calculated as Average Invoiced Price - Cost price
* Gross Margin on invoices (%): Gross Margin on invoices rate
* Total Margin on cost: calculated as Gross Margin on invoices * qty

All prices are in the company's main currency

Backround
---------
This modules depends on module invoice_report_extra_groupby
which add in the invoice lines the total amount converted to the company's
currency.

Contributors
------------
* Marc Cassuto (marc.cassuto@gmail.com)
""",
    'depends': [
        'account',
        'invoice_report_extra_groupby'
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'report_invoice_margin_view.xml',
    ],
    'installable': True,
}
