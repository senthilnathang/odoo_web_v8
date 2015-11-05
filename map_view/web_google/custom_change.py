# -*- coding: utf-8 -*-

from openerp.osv import osv, fields


class view(osv.osv):
    _inherit = 'ir.ui.view'

    _columns = {
        'type': fields.selection([
            ('tree', 'Tree'),
            ('form', 'Form'),
            ('graph', 'Graph'),
            ('map', 'Map'),
            ('calendar', 'Calendar'),
            ('diagram', 'Diagram'),
            ('gantt', 'Gantt'),
            ('kanban', 'Kanban'),
            ('search', 'Search'),
            ('qweb', 'QWeb')], string='View Type'),
        }

view()


class ir_actions_act_window(osv.osv):
    _inherit = 'ir.actions.act_window'

VIEW_TYPES = [
    ('tree', 'Tree'),
    ('form', 'Form'),
    ('graph', 'Graph'),
    ('map', 'Map'),
    ('calendar', 'Calendar'),
    ('gantt', 'Gantt'),
    ('kanban', 'Kanban')]

ir_actions_act_window()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
