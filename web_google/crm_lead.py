# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2015-Today BrowseInfo (<http://www.browseinfo.in>)
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

from openerp.osv import osv
from openerp.osv import fields


class crm_lead(osv.osv):
    _inherit = 'crm.lead'

    def action_schedule_meeting(self, cr, uid, ids, context=None):
        res = super(crm_lead, self).action_schedule_meeting(
            cr, uid, ids, context=context)
        lead = self.browse(cr, uid, ids[0], context)
        res['context'].update(
            {'default_city': lead.partner_id.city or False,
             'default_country_id': lead.partner_id.country_id and
             lead.partner_id.country_id.id or False,
             'default_state_id': lead.partner_id.state_id and
             lead.partner_id.state_id.id or False
             })
        return res


crm_lead()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
