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

import openerp
import urlparse
import werkzeug
from openerp.osv import orm

from openerp.osv import osv,  fields

class res_company(osv.Model):
    """override company to add google map api"""
    _inherit = "res.company"
    
    _columns = {
    'google_api_key': fields.char("Google Map API Key")
              }    


def urlplus(url, params):
    return werkzeug.Href(url)(params or None)
    
class website(orm.Model):
    _inherit = 'website'
    
    def google_map_src(self, cr, uid, ids, zoom=8,context=None):
        user = self.browse(cr, openerp.SUPERUSER_ID, ids[0], context=context)
        partner = self.pool.get('res.partner').browse(cr, uid, user.company_id.partner_id.id, context=context)
        params = {
            'key':user.company_id and user.company_id.google_api_key or "",
            'q': '%s,%s, %s %s, %s' % (user.company_id.name or '',partner.street or '', partner.city  or '', partner.zip or '', partner.country_id and partner.country_id.name_get()[0][1] or ''),
        }
        print params
        return urlplus('https://www.google.com/maps/embed/v1/place' , params)
