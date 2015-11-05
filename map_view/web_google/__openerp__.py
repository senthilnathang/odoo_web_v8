# -*- coding: utf-8 -*-

{
    'name': 'Map Views',
    'category': 'Hidden',
    'description': """
Map Views for Web Client.
===========================
""",
    'version': '3.0',
    'depends': ['base', 'web', 'sale',
                'crm', 'sale_commission',
                'calendar'
                ],
    'data': [
        'views/web_map.xml',
        'custom_view_map.xml',
        'calendar_view.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'auto_install': True
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
