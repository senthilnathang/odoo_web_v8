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
    'name': 'BrowseInfo E-commerce Theme',
    'summary': 'HTML5 Multi-purpose Responsive Bootstrap Theme for Odoo CMS By BrowseInfo',
    'category': 'Theme/E-Commerce',
    'version': '1.0',
    'website': 'www.browseinfo.in',
    'author': 'BrowseInfo',
    'description': """
BrowseInfo, as the name suggests, Our work speaks for itself, so therefore we mean business and creativity. All of the clients are satisfied with our work. So check some of our creative picks and judge by yourself. This theme is also one of our creativity. With a range of features to give handy tool to customize the theme simply, Browseinfo is the one that can be redefined to create an awesome website.
===================

        """,
    'depends': ['website','website_sale'], #'mass_mailing_distribution_list'
    'data': [
        'views/res_company.xml',          
        'views/partner_view.xml',
        'views/product_view.xml',
        'views/product_config_view.xml',
        'data/data.xml',
        'views/theme.xml', 
        'views/product_template.xml',
    ],
    'images': ['static/description/005.png'],
    'price': 100.00,
    'currency': 'EUR',
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
