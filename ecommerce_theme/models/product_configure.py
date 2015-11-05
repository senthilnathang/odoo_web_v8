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

from openerp import api, fields, models
from openerp.models import Model


class website(Model):

    """Adds the fields for options of the Zooming."""

    _inherit = 'website'

    is_zoom_feature = fields.Boolean(
        string='Do you want to disable zooming feature',
        default=False,) 
    inner_zoom = fields.Boolean(
        string='Do you want to enable inner zooming feature',
        default=False,)    

class WebsiteConfigSettings(models.TransientModel):

    """Settings for the Zoom."""

    _inherit = 'website.config.settings'
    
    is_zoom_feature = fields.Boolean(
        related='website_id.is_zoom_feature',
        string="Do you want to disable zooming feature?")  
    inner_zoom = fields.Boolean(
        string='Do you want to enable inner zooming feature',
        related='website_id.inner_zoom')      

      

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
