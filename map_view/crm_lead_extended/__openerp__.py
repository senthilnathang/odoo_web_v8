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
{
    "name" : "CRM Lead Extended",
    "author" : "Browseinfo",
    "version" : "1.0",
    "depends" : ['crm', 'base', 'sale', 'email_template', 'calendar', 'account', 'product', 'sales_team', 'account_voucher', 'sale_crm', 'sale_commission', 'stock'],
    "description": """
        This module is for CRM.
    """,
    "website" : "www.browseinfo.in",
    "data" :[
            'security/ir.model.access.csv',
			'crm_lead_data.xml',
			'crm_lead_extended_view.xml',
			'crm_sequence.xml',
    ],
    'qweb': ['static/src/xml/google_map_locator.xml'],
    "auto_install": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
