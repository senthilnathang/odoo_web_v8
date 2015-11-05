# -*- coding: utf-8 -*-

from openerp.osv import osv, orm, fields
from datetime import date
from openerp.addons.website.models.website import slugify

class product_template(osv.Model):
    _inherit = "product.template"    
    _columns = {
                'is_arrival':fields.boolean('Arrival Products'),
                'is_features': fields.boolean('Feature Products'),
    }    
    _defaults = {
                 'is_arrival':False,
                 'is_features':False,
    }
product_template()

class res_partner(osv.osv):
    _description = 'Supplier Brand'
    _inherit = "res.partner"
    _columns={                               
              'is_home_brand':fields.boolean('Brand'),             
    }
    _defaults = {
                 'is_home_brand':False,     
    }    
res_partner()

class website(orm.Model):
    _inherit = 'website'
      
    def get_arrival_product(self, cr, uid,ids, context=None):        
        prod_ids=self.pool.get('product.template').search(cr, uid, [('is_arrival','=','True'),("sale_ok", "=", True)], context=context)
        if prod_ids and len(prod_ids)>16:
            prod_ids=prod_ids[:16]
        elif prod_ids and len(prod_ids)<=16:
            prod_ids=prod_ids
        price_list=self.price_list_get(cr,uid,context);
        product_data = self.pool.get('product.template').browse(cr,uid,prod_ids,{'pricelist':int(price_list)})
        return product_data    
    
    def price_list_get(self,cr,uid,context=None):
            partner = self.pool.get('res.users').browse(cr, uid, uid, context=context)
            if partner:
                price_list=partner.partner_id.property_product_pricelist
                return price_list.id
            return True
    
    def get_feature_product(self, cr, uid,ids, context=None):            
        prod_ids=self.pool.get('product.template').search(cr, uid,[('is_features','=','True'),("sale_ok", "=", True)], context=context)
        if prod_ids and len(prod_ids)>8:
            prod_ids=prod_ids[:8]
        elif prod_ids and len(prod_ids)<=8:
            prod_ids=prod_ids
        price_list=self.price_list_get(cr,uid,context);
        product_data = self.pool.get('product.template').browse(cr,uid,prod_ids,{'pricelist':int(price_list)})
        return product_data
        
    def get_brand_img(self, cr, uid,ids, context=None):    
        brand_ids=self.pool.get('res.partner').search(cr, uid, [('is_home_brand','=','True')], context=context)
        brand_data = self.pool.get('res.partner').browse(cr,uid,brand_ids,context)
        return brand_data
    
    def get_current_year(self):
        return date.today().year

    def new_page(self, cr, uid, name, template='website.default_page', ispage=True, context=None):
        context = context or {}
        imd = self.pool.get('ir.model.data')
        view = self.pool.get('ir.ui.view')
        template_module, template_name = template.split('.')

        # completely arbitrary max_length
        page_name = slugify(name, max_length=50)
        page_xmlid = "%s.%s" % (template_module, page_name)

        try:
            # existing page
            imd.get_object_reference(cr, uid, template_module, page_name)
        except ValueError:
            # new page
            _, template_id = imd.get_object_reference(cr, uid, template_module, template_name)
            page_id = view.copy(cr, uid, template_id, context=context)
            page = view.browse(cr, uid, page_id, context=context)
            page.write({
                'arch': page.arch.replace(template, page_xmlid),
                'name': page_name,
                'page': ispage,
            })
            page1=view.browse(cr, uid, page_id, context=context)
            arch='<?xml version="1.0"?><t t-name="website.'+str(page_name)+'"><t t-call="website.layout"> \
                    <div id="wrap" class="oe_structure oe_empty"><div class="page-title"><div class="container">\
                    <h1>'+str(page_name.capitalize())+'</h1> \
                    <ul class="breadcrumb"><li><a href="/page/homepage">Home</a>\
                    </li><li class="active">'+str(page_name.capitalize())+'</li></ul></div></div></div></t></t>'
            page1.write({'arch':arch})
            imd.create(cr, uid, {
                'name': page_name,
                'module': template_module,
                'model': 'ir.ui.view',
                'res_id': page_id,
                'noupdate': True
            }, context=context)
        return page_xmlid
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
