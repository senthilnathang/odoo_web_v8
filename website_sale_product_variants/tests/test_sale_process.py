# -*- coding: utf-8 -*-
##############################################################################
#
#    Sales and Account Invoice Discount Management
#    Copyright (C) 2015 BrowseInfo(<http://www.browseinfo.in>).
#    $autor:
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


import openerp.tests

@openerp.tests.common.at_install(False)
@openerp.tests.common.post_install(True)
class TestUi(openerp.tests.HttpCase):
    def test_01_admin_shop_tour(self):
        self.phantom_js("/", "openerp.Tour.run('shop', 'test')", "openerp.Tour.tours.shop", login="admin")

    def test_02_admin_checkout(self):
        self.phantom_js("/", "openerp.Tour.run('shop_buy_product', 'test')", "openerp.Tour.tours.shop_buy_product", login="admin")

    def test_03_demo_checkout(self):
        self.phantom_js("/", "openerp.Tour.run('shop_buy_product', 'test')", "openerp.Tour.tours.shop_buy_product", login="demo")

    def test_04_public_checkout(self):
        self.phantom_js("/", "openerp.Tour.run('shop_buy_product', 'test')", "openerp.Tour.tours.shop_buy_product")
        
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:        
