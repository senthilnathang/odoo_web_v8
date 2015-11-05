# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp.osv import fields


class crm_lead(osv.osv):
    _inherit = 'crm.lead'

    def action_schedule_meeting(self, cr, uid, ids, context=None):
        res = super(crm_lead, self).action_schedule_meeting(cr, uid, ids, context=context)
        lead = self.browse(cr, uid, ids[0], context)
        res['context'].update(
            {'default_city': lead.partner_id.city or False,
             'default_country_id': lead.partner_id.country_id and lead.partner_id.country_id.id or False,
             'default_state_id': lead.partner_id.state_id and lead.partner_id.state_id.id or False
             })
        return res


crm_lead()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
