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

from openerp.osv import osv,  fields

class subscribe_website(osv.Model):
    _inherit='res.partner'
    _columns={
              'subscribe':fields.boolean("Subscribe",help="Subscribe"),
              }
    def create(self, cr, uid, vals, context=None):
        if vals.has_key('email') and vals['email']:
            subscribe_customer=self.search(cr,uid,[('subscribe','=',True),('email','=',vals['email'])])
            if subscribe_customer:
                vals.update({'subscribe' :True})
                self.write(cr,uid,subscribe_customer,vals)
                return subscribe_customer[0]
        return super(subscribe_website,self).create(cr,uid,vals,context)

subscribe_website()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
