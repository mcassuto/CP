# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Marc Cassuto.
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

import time

from openerp.osv import fields, osv


class ProductProduct(osv.osv):
    _inherit = "product.product"

    def _product_margin(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        if context is None:
            context = {}

        for val in self.browse(cr, uid, ids, context=context):
            res[val.id] = {}
            date_from = context.get('date_from', time.strftime('%Y-01-01'))
            date_to = context.get('date_to', time.strftime('%Y-12-31'))
            invoice_state = context.get('invoice_state', 'open_paid')
            if 'date_from' in field_names:
                res[val.id]['date_from'] = date_from
            if 'date_to' in field_names:
                res[val.id]['date_to'] = date_to
            if 'invoice_state' in field_names:
                res[val.id]['invoice_state'] = invoice_state

            states = ()
            if invoice_state == 'paid':
                states = ('paid',)
            elif invoice_state == 'open_paid':
                states = ('open', 'paid')
            elif invoice_state == 'draft_open_paid':
                states = ('draft', 'open', 'paid')

            sqlstr = """select
                    sum(l.price_unit * l.quantity)/sum(nullif(l.quantity,0))
                      as avg_unit_price,
                    sum(l.quantity) as num_qty,
                    sum(l.quantity * (l.price_subtotal/(nullif(l.quantity,0))))
                      as total,
                    sum(l.quantity * pt.list_price) as sale_expected,
                    sum(l.quantity * pt.standard_price) as normal_cost
                from account_invoice_line l
                left join account_invoice i on (l.invoice_id = i.id)
                left join product_product product on (product.id=l.product_id)
                left join product_template pt
                  on (pt.id=product.product_tmpl_id)
                where l.product_id = %s
                 and i.state in %s
                 and i.type IN %s
                 and (i.date_invoice IS NULL
                      or (i.date_invoice>=%s and i.date_invoice<=%s))
                """
            invoice_types = ('out_invoice', 'in_refund')
            cr.execute(sqlstr,
                       (val.id, states, invoice_types, date_from, date_to))
            result = cr.fetchall()[0]
            res[val.id]['sale_avg_price'] = result[0] and result[0] or 0.0
            res[val.id]['sale_num_invoiced'] = result[1] and result[1] or 0.0
            res[val.id]['turnover'] = result[2] and result[2] or 0.0
            res[val.id]['sale_expected'] = result[3] and result[3] or 0.0
            res[val.id]['sales_gap'] =\
                res[val.id]['sale_expected']-res[val.id]['turnover']

            invoice_types = ('in_invoice', 'out_refund')
            cr.execute(sqlstr,
                       (val.id, states, invoice_types, date_from, date_to))
            result = cr.fetchall()[0]
            res[val.id]['purchase_avg_price'] =\
                result[0] and result[0] or 0.0
            res[val.id]['purchase_num_invoiced'] =\
                result[1] and result[1] or 0.0
            res[val.id]['total_cost'] = result[2] and result[2] or 0.0
            res[val.id]['normal_cost'] = result[4] and result[4] or 0.0
            res[val.id]['purchase_gap'] =\
                res[val.id]['normal_cost']-res[val.id]['total_cost']

            if 'total_margin' in field_names:
                res[val.id]['total_margin'] =\
                    res[val.id]['turnover'] - res[val.id]['total_cost']
            if 'expected_margin' in field_names:
                res[val.id]['expected_margin'] =\
                    res[val.id]['sale_expected'] - res[val.id]['normal_cost']
            if 'total_margin_rate' in field_names:
                res[val.id]['total_margin_rate'] =\
                    res[val.id]['turnover'] and\
                    res[val.id]['total_margin'] *\
                    100 / res[val.id]['turnover'] or 0.0
            if 'expected_margin_rate' in field_names:
                res[val.id]['expected_margin_rate'] =\
                    res[val.id]['sale_expected'] and\
                    res[val.id]['expected_margin'] *\
                    100 / res[val.id]['sale_expected'] or 0.0
            # Calculations added in this module
            if 'th_gross_margin' in field_names:
                res[val.id]['th_gross_margin'] =\
                    val.list_price - val.standard_price
            if 'th_gross_margin_rate' in field_names:
                res[val.id]['th_gross_margin_rate'] =\
                    res[val.id]['th_gross_margin']
            if 'gross_margin' in field_names:
                res[val.id]['gross_margin'] =\
                    res[val.id]['sale_avg_price'] - val.standard_price
            if 'gross_margin_rate' in field_names:
                res[val.id]['gross_margin_rate'] =\
                    res[val.id]['gross_margin']
            if 'total_margin_on_cost' in field_names:
                res[val.id]['total_margin_on_cost'] =\
                    res[val.id]['turnover'] -\
                    (res[val.id]['sale_num_invoiced'] * val.standard_price)

        return res

    _columns = {
        # Override this field ot have it stored; needed for the search view
        'sale_num_invoiced' : fields.function(
            _product_margin,
            type='float',
            string='# Invoiced in Sale',
            multi='product_margin',
            store=True,
            help="Sum of Quantity in Customer Invoices"),
        # New columns
        'th_gross_margin': fields.function(
            _product_margin,
            type='float',
            string='Gross Margin on list price',
            multi='product_margin',
            help="List price - Cost price"),
        'th_gross_margin_rate': fields.function(
            _product_margin,
            type='float',
            string='Gross Margin on list price (%)',
            multi='product_margin',
            help="Gross Margin on list price * 100 / Cost price"),
        'gross_margin': fields.function(
            _product_margin,
            type='float',
            string='Gross Margin on invoices',
            multi='product_margin',
            help="Average Invoiced Price - Cost price"),
        'gross_margin_rate': fields.function(
            _product_margin,
            type='float',
            string='Gross Margin on invoices (%)',
            multi='product_margin',
            help="Gross Margin on invoices * 100 / Cost price"),
        'total_margin_on_cost': fields.function(
            _product_margin,
            type='float',
            string='Total Margin on cost',
            multi='product_margin',
            help="Total invoiced - Total cost (on standard price)"),

    }

ProductProduct()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
