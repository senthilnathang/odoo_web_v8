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
    'name': 'Browseinfo',
    'category': 'Website',
    'summary': 'Erp-Browseinfo Website',
    'website': 'www.browseinfo.in',
    'version': '1.0',
    'description': """
BrowseInfo is a global IT services company focusing on software development, IT consulting and provides offshore outsourcing solutions to enterprises worldwide. It has the required development facilities and infrastructure combined with quality assurance processes to ensure timely delivery of high quality and low maintenance Web & Software solutions.
===================

        """,
    'author': 'BrowseInfo',
    'depends': ['website','sale','website_hr_recruitment_custom'],
    'installable': True,
    'data': [
        'data/data.xml',
        'views/template.xml',
    ],
    'application': True,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
