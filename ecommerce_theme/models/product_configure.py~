# -*- coding: utf-8 -*-

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
