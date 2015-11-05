# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from openerp.osv import osv, orm, fields

class product_category(osv.Model):
    _inherit='product.public.category'
    _columns={
              'include_in_menu':fields.boolean("Include in Navigation Menu",help="Include in Navigation Menu"),
              }

product_category()

class website(orm.Model):
    _inherit = 'website'
    
    def get_product_category(self, cr, uid,ids, context=None):  
        category_ids=self.pool.get('product.public.category').search(cr,uid,[('parent_id', '=', False),('include_in_menu','!=',False)])
        if category_ids and len(category_ids)>5:
            category_ids=category_ids[:5]
        elif category_ids and len(category_ids)<=5:
            category_ids=category_ids
        category_data = self.pool.get('product.public.category').browse(cr,uid,category_ids,context)
        return category_data

    def get_product_child_category(self, cr, uid,ids,child_id,context=None):  
        category_ids=self.pool.get('product.public.category').search(cr,uid,[('parent_id', '=', child_id),('include_in_menu','!=',False)],order="sequence asc")        
        category_data = self.pool.get('product.public.category').browse(cr,uid,category_ids,context)
        return category_data
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:        
