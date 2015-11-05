# -*- coding: utf-8 -*-

from openerp.osv import osv, orm, fields

class product_images(osv.Model):
    _name = 'product.images'
    _description="Add Multiple Image in Product"

    _columns = {
        'name': fields.char('Label'),
        'image': fields.binary('Image'),
        'sequence':fields.integer('Sort Order'),
        'product_tmpl_id': fields.many2one('product.template', 'Product'),
        'more_view_exclude':fields.boolean("More View Exclude"),
    }
product_images()


class product_template(osv.Model):
    _inherit = 'product.template'
    _description="Multiple Images"    

    _columns = {
        'images': fields.one2many('product.images', 'product_tmpl_id',
                                  string='Images'),
        'multi_image':fields.boolean("Add Multiple Images?"),
    }
product_template()

class website(orm.Model):
    _inherit = 'website'
    
    def get_multiple_images(self, cr, uid,product_id=None,context=None):
        product_img_data=False
        print product_id
        if product_id:
            cr.execute('select id from product_images where product_tmpl_id=%s and more_view_exclude IS NOT TRUE order  by sequence',([product_id]))
            product_ids=map(lambda x: x[0], cr.fetchall())
            if product_ids:
                product_img_data=self.pool.get('product.images').browse(cr,uid,product_ids,context)
        return product_img_data
    
    def get_zoom_feature(self,cr,uid,context=None):
        zoom=self.pool.get('product.multiple.image.config').search(cr,uid,[('is_zoom_feature','=',True)])
        if zoom:
            return True
        else:
            return False
    def get_image_url(self, cr, uid, record, field, size=None, context=None):
        """Returns a local url that points to the image field of a given browse record."""
        model = record._name
        sudo_record = record.sudo()
        id = '%s_%s' % (record.id, hashlib.sha1(sudo_record.write_date or sudo_record.create_date or '').hexdigest()[0:7])
        size = '' if size is None else '/%s' % size
        return '/website/image/%s/%s/%s%s' % (model, id, field, size)
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

                


