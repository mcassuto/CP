# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
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


class StockWarehouseOrderpoint(osv.osv):
    _inherit = "stock.warehouse.orderpoint"

    def _product_available(self, cr, uid, ids, field_names=None, arg=False,
                           context=None):
        """ Finds the incoming and outgoing quantity of product.
        @return: Dictionary of values
        """
        product_obj = self.pool.get('product.product')

        res = {}
        if context is None:
            context = {}

        for val in self.browse(cr, uid, ids, context=context):
            res[val.id] = {}

            # Compute Quantity On Hand
            states = ('done',)
            c = context.copy()
            c.update({'states': states,
                      'what': ('in', 'out'),
                      'location': val.location_id.id,
                      'product_id': val.product_id.id})
            result = product_obj.get_product_available(cr,
                                                       uid,
                                                       [val.product_id.id],
                                                       context=c)
            res[val.id]['qty_available'] = result[val.product_id.id]

            # Compute Virtual Quantity
            states = ('confirmed', 'waiting', 'assigned', 'done')
            c = context.copy()
            c.update({'states': states,
                      'what': ('in', 'out'),
                      'location': val.location_id.id,
                      'product_id': val.product_id.id})
            result = product_obj.get_product_available(cr,
                                                       uid,
                                                       [val.product_id.id],
                                                       context=c)
            res[val.id]['virtual_available'] = result[val.product_id.id]

        return res

    _columns = {
        'qty_available': fields.function(
            _product_available,
            type='float',
            multi='qty_available',
            string='Quantity On Hand',
            help="Quantity available at this location"),
        'virtual_available': fields.function(
            _product_available,
            type='float',
            multi='qty_available',
            string='Forecasted Quantity',
            help="Forecasted Quantity at this location \
                (computed as Quantity On Hand - Outgoing + Incoming)"),
    }
