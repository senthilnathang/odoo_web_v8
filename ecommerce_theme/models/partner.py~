# -*- coding: utf-8 -*-

from openerp.osv import osv,  fields

class subscribe_website(osv.Model):
    _inherit='res.partner'
    _columns={
              'subscribe':fields.boolean("Subscribe",help="Subscribe"),
              }
    def create(self, cr, uid, vals, context=None):
        if vals.has_key('email') and vals['email']:
            subscribe_customer=self.search(cr,uid,[('subscribe','=',True),('email','=',vals['email'])])
            if subscribe_customer:
                vals.update({'subscribe' :True})
                self.write(cr,uid,subscribe_customer,vals)
                return subscribe_customer[0]
        return super(subscribe_website,self).create(cr,uid,vals,context)

subscribe_website()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: