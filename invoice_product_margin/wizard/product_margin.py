# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Marc Cassuto <marc.cassuto@gmail.com>.
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

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta


class InvoiceProductMarginWizard(osv.osv_memory):
    _name = 'invoice.product.margin.wizard'
    _description = 'Product Margin on Invoices)'
    _columns = {
        'from_date': fields.date('From'),
        'to_date': fields.date('To'),
    }
    _defaults = {
        'from_date': lambda *a: (
            parser.parse(datetime.now().strftime('%Y-%m-01')) +
            relativedelta(months=-1)
        ).strftime('%Y-%m-%d'),
        'to_date': lambda *a: (
            parser.parse(datetime.now().strftime('%Y-%m-01')) +
            relativedelta(days=-1)
        ).strftime('%Y-%m-%d'),
    }

    def action_open_window(self, cr, uid, ids, context=None):
        """
            @param cr: the current row, from the database cursor,
            @param uid: the current user’s ID for security checks,
            @param ids: the ID or list of IDs if we want more than one

            @return:
        """
        if context is None:
            context = {}
        mod_obj = self.pool.get('ir.model.data')
        result = mod_obj._get_id(cr, uid,
                                 'invoice_product_margin',  # Module name
                                 'view_invoice_margins_report_search')
        search_view_id = mod_obj.read(cr, uid, result,
                                      ['res_id'],
                                      context=context)

        # Get the tree view id
        cr.execute(
            'select id, name from ir_ui_view where name=%s and type=%s',
            ('invoice.margins.report.tree', 'tree')
        )
        tree_view_res = cr.fetchone()[0]

        # get the current product.margin object to obtain the values from it
        wizard_obj = self.browse(cr, uid, ids, context=context)[0]

        if wizard_obj.from_date:
            context.update(date_from=wizard_obj.from_date)
        if wizard_obj.to_date:
            context.update(date_to=wizard_obj.to_date)

        context.update({'search_default_product': 1, 'group_by_no_leaf': 1})

        return {
            'name': _('Product Margin on Invoices'),
            'context': context,
            'view_type': 'form',
            "view_mode": 'tree',
            'res_model': 'invoice.product.margin',
            'type': 'ir.actions.act_window',
            'views': [(tree_view_res, 'tree')],
            'view_id': False,
            'search_view_id': search_view_id['res_id'],
        }

InvoiceProductMarginWizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
