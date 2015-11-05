# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp.osv import fields


class calendar_event(osv.osv):
    _inherit = 'calendar.event'

    _columns = {

        'city': fields.char('City', size=64,),
        'state_id': fields.many2one('res.country.state', 'State', ),
        'country_id': fields.many2one('res.country', 'Country'),
    }

calendar_event()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
