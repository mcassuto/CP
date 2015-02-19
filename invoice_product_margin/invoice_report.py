##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp import tools
from openerp.osv import fields, osv


class InvoiceProductMargin(osv.osv):
    _name = 'invoice.product.margin'
    _auto = False
    _rec_name = 'date'

    _columns = {
        'date': fields.date(
            'Date',
            readonly=True),
        'partner_id': fields.many2one(
            'res.partner',
            'Partner',
            readonly=True),
        'product_id': fields.many2one(
            'product.product',
            'Product',
            readonly=True),
        'product_qty': fields.float(
            'Qty',
            readonly=True),
        'standard_price': fields.float(
            'Manuf. Cost',
            readonly=True,
            group_operator="avg"),
        'list_price': fields.float(
            'List Price',
            readonly=True,
            group_operator="avg"),
        'price_average': fields.float(
            'Avg. Inv. Price',
            readonly=True,
            group_operator="avg"),
        'invoice_id': fields.many2one(
            'account.invoice',
            'Invoice',
            readonly=True),
        'total_in_main_currency': fields.float(
            'Total',
            readonly=True),
        'th_gross_margin': fields.float(
            'Gross Margin on list price',
            readonly=True,
            group_operator="avg",
            help="List price - Cost price"),
        'th_gross_margin_rate': fields.float(
            'Gross Margin on list price (%)',
            readonly=True,
            group_operator="avg",
            help="Gross Margin on list price * 100 / Cost price"),
        'gross_margin': fields.float(
            'Gross Margin on invoices',
            readonly=True,
            group_operator="avg",
            help="Average Invoiced Price - Cost price"),
        'gross_margin_rate': fields.float(
            'Gross Margin on invoices (%)',
            readonly=True,
            group_operator="avg",
            help="Gross Margin on invoices * 100 / Cost price"),
        'total_margin_on_cost': fields.float(
            'Total Margin on cost',
            readonly=True,
            group_operator="sum",
            help="Total invoiced - Total cost (on standard price)"),
    }

    _order = 'product_id'

    def _select(self):
        select_str = """
            SELECT sub.id, sub.date, sub.currency_id, sub.partner_id,
                sub.product_id, sub.product_qty, sub.invoice_id as invoice_id,
                sub.price_total_in_currency as total_in_main_currency,
                sub.standard_price, sub.list_price,
                (sub.list_price - sub.standard_price) as th_gross_margin,
                ( (sub.list_price - sub.standard_price) * 100 / nullif(sub
                    .standard_price,0)) as th_gross_margin_rate,
                ( sub.price_total_in_currency / nullif(sub.product_qty,
                    0) ) as price_average,
                ( (sub.price_total_in_currency / nullif(sub.product_qty,
                    0)) - standard_price) as gross_margin,
                ( ((sub.price_total_in_currency / nullif(sub.product_qty,
                    0)) - standard_price) * 100 / nullif(sub.standard_price,
                    0)) as gross_margin_rate,
                ( ((sub.price_total_in_currency / nullif(sub.product_qty,
                    0 )) - standard_price) * sub.product_qty)
                    as total_margin_on_cost
        """
        return select_str

    def _sub_select(self):
        select_str = """
                SELECT min(ail.id) AS id,
                    ai.date_invoice AS date, ai.partner_id,
                    ai.currency_id, ail.product_id,
                    SUM(CASE
                        WHEN ai.type::text = ANY (
                            ARRAY['out_refund'::character varying::text,
                            'in_invoice'::character varying::text]
                            )
                            THEN (- ail.quantity) / u.factor
                            ELSE ail.quantity / u.factor
                        END) AS product_qty,
                    ai.id as invoice_id,
                    SUM(CASE
                        WHEN ai.type::text = ANY (
                            ARRAY['out_refund'::character varying::text,
                            'in_invoice'::character varying::text]
                            )
                            THEN - ail.price_subtotal_in_currency
                            ELSE ail.price_subtotal_in_currency
                        END) AS price_total_in_currency,
                    pt.standard_price, pt.list_price
        """
        return select_str

    def _sub_from(self):
        # date_from = context.get('date_from', time.strftime('%Y-01-01'))
        # date_to = context.get('date_to', time.strftime('%Y-12-31'))
        # print date_from
        # print date_to
        from_str = """
                FROM account_invoice_line ail
                JOIN account_invoice ai ON ai.id = ail.invoice_id
                LEFT JOIN product_product pr ON pr.id = ail.product_id
                LEFT JOIN product_template pt ON pt.id = pr.product_tmpl_id
                LEFT JOIN product_uom u ON u.id = ail.uos_id
                WHERE ai.type in ('out_invoice','out_refund')
                    AND ai.state in ('open', 'paid')
        """
        return from_str

    def _sub_group_by(self):
        group_by_str = """
                GROUP BY ail.product_id, ai.date_invoice, ai.id, ai.partner_id,
                    ai.currency_id, pt.standard_price, pt.list_price
        """
        return group_by_str

    def init(self, cr, context=None):
        # self._table = account_invoice_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM (
                %s %s %s
            ) AS sub
            JOIN res_currency_rate cr ON (cr.currency_id = sub.currency_id)
            WHERE
                cr.id IN (
                    SELECT id
                    FROM res_currency_rate cr2
                    WHERE (cr2.currency_id = sub.currency_id)
                        AND ((sub.date IS NOT NULL AND cr2.name <= sub.date)
                            OR (sub.date IS NULL AND cr2.name <= NOW()))
                    ORDER BY name DESC LIMIT 1)
        )""" % (self._table,
                self._select(),
                self._sub_select(),
                self._sub_from(),
                self._sub_group_by()
                )
        )

InvoiceProductMargin()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
