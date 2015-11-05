
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
# -*- coding: utf-8 -*-

import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug

class website_browseinfo(http.Controller):

   
    @http.route('/services/', type='http', auth="public", website=True)
    def services(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        
        
        return request.website.render("browseinfo.services")
        
    @http.route('/http://browseinfo.in/blog/', type='http', auth="public", website=True)
    def blog(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        
        return werkzeug.utils.redirect("/myNewPage",301)
        
        

    @http.route(['/odoo'], type='http', auth="public", website=True)
    def odoo(self, page=0, category=None, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        
        return request.website.render("browseinfo.odoo")
        
        
    '''@http.route(['/career'], type='http', auth="public", website=True)
    def career(self, page=0, category=None, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        
        return request.website.render("browseinfo.career")'''
        
    @http.route(['/about'], type='http', auth="public", website=True)
    def about(self, page=0, category=None, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        
        return request.website.render("browseinfo.about")

    @http.route(['/contact'], type='http',auth="public", website=True)
    def contact(self, page=0, category=None, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        return request.website.render("browseinfo.contact")



# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
