# -*- coding: utf-8 -*-
import base64

from openerp import SUPERUSER_ID
from openerp import http
from openerp.tools.translate import _
from openerp.http import request
from openerp.addons.website.models.website import slug


class website_hr_recruitment_custom(http.Controller):
    @http.route([
        '/jobs',
        '/jobs/country/<model("res.country"):country>',
        '/jobs/department/<model("hr.department"):department>',
        '/jobs/country/<model("res.country"):country>/department/<model("hr.department"):department>',
        '/jobs/office/<int:office_id>',
        '/jobs/country/<model("res.country"):country>/office/<int:office_id>',
        '/jobs/department/<model("hr.department"):department>/office/<int:office_id>',
        '/jobs/country/<model("res.country"):country>/department/<model("hr.department"):department>/office/<int:office_id>',
    ], type='http', auth="public", website=True)
    def jobs(self, country=None, department=None, office_id=None, **kwargs):
        env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))

        Country = env['res.country']
        Jobs = env['hr.job']

        # List jobs available to current UID
        job_ids = Jobs.search([], order="website_published desc,no_of_recruitment desc").ids
        # Browse jobs as superuser, because address is restricted
        jobs = Jobs.sudo().browse(job_ids)

        # Deduce departments and offices of those jobs
        departments = set(j.department_id for j in jobs if j.department_id)
        offices = set(j.address_id for j in jobs if j.address_id)
        countries = set(o.country_id for o in offices if o.country_id)

        # Default search by user country
        if not (country or department or office_id or kwargs.get('all_countries')):
            country_code = request.session['geoip'].get('country_code')
            if country_code:
                countries_ = Country.search([('code', '=', country_code)])
                country = countries_[0] if countries_ else None
                if not any(j for j in jobs if j.address_id and j.address_id.country_id == country):
                    country = False

        # Filter the matching one
        if country and not kwargs.get('all_countries'):
            jobs = (j for j in jobs if j.address_id is None or j.address_id.country_id and j.address_id.country_id.id == country.id)
        if department:
            jobs = (j for j in jobs if j.department_id and j.department_id.id == department.id)
        if office_id:
            jobs = (j for j in jobs if j.address_id and j.address_id.id == office_id)

        # Render page
        return request.website.render("website_hr_recruitment_custom.index", {
            'jobs': jobs,
            'countries': countries,
            'departments': departments,
            'offices': offices,
            'country_id': country,
            'department_id': department,
            'office_id': office_id,
        })

    @http.route('/jobs/add', type='http', auth="user", website=True)
    def jobs_add(self, **kwargs):
        job = request.env['hr.job'].create({
            'name': _('New Job Offer'),
        })
        return request.redirect("/jobs/detail/%s?enable_editor=1" % slug(job))

    @http.route('/jobs/detail/<model("hr.job"):job>', type='http', auth="public", website=True)
    def jobs_detail(self, job, **kwargs):
        return request.render("website_hr_recruitment_custom.detail", {
            'job': job,
            'main_object': job,
        })

    @http.route('/jobs/apply/<model("hr.job"):job>', type='http', auth="public", website=True)
    def jobs_apply(self, job):
        error = {}
        default = {}
        if 'website_hr_recruitment_error' in request.session:
            error = request.session.pop('website_hr_recruitment_error')
            default = request.session.pop('website_hr_recruitment_default')
        return request.render("website_hr_recruitment_custom.apply", {
            'job': job,
            'error': error,
            'default': default,
        })

    @http.route('/jobs/thankyou', methods=['POST'], type='http', auth="public", website=True)
    def jobs_thankyou(self, **post):
        error = {}
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        for field_name in ["partner_name", "phone", "email_from"]:
            if not post.get(field_name):
                error[field_name] = 'missing'
        if error:
            request.session['website_hr_recruitment_error'] = error
            ufile = post.pop('ufile')
            if ufile:
                error['ufile'] = 'reset'
            request.session['website_hr_recruitment_default'] = post
            return request.redirect('/jobs/apply/%s' % post.get("job_id"))

        # public user can't create applicants (duh)
        env = request.env(user=SUPERUSER_ID)
        value = {
            'source_id': env.ref('hr_recruitment.source_website_company').id,
            'name': '%s\'s Application' % post.get('partner_name'),
        }
        res_users = request.registry.get('res.users')
        res_vals = {
            'name': post.get('partner_name'),
            'login': post.get('email_from'),
            'email': post.get('email_from'),
                   }
        new_res_users = res_users.create(cr, SUPERUSER_ID, res_vals, context=context)
        print "ahiiii patyu.......!!!! and p6i access rights apya niche"
        access=request.registry.get('res.groups')
        ir_mod_cat=request.registry.get('ir.module.category')
        ir_mod_cat_id=ir_mod_cat.search(cr,SUPERUSER_ID,[('name','=','Human Resources')],context=context)
        print "\n)))))))))))))))))))))))))))))",new_res_users,"\ncate====",ir_mod_cat_id
        if ir_mod_cat_id:
            hr_search_id=access.search(cr,SUPERUSER_ID,[('category_id','=',ir_mod_cat_id[0]),('name','=','Manager')],context=context)
            print "hr_search_id=====>>>>",hr_search_id
            hr_search_id_del=access.search(cr,SUPERUSER_ID,[('category_id','=',ir_mod_cat_id[0]),('name','=','Employee')],context=context)
        access_user=access.search(cr,SUPERUSER_ID,[('name','=','Survey / User')],context=context)
        grp_users=access.write(cr,SUPERUSER_ID,access_user,{'users': [(4,new_res_users)]},context)
        grp_users=access.write(cr,SUPERUSER_ID,hr_search_id_del,{'users': [(3,new_res_users)]},context)
        grp_users=access.write(cr,SUPERUSER_ID,hr_search_id,{'users': [(4,new_res_users)]},context)
        print access_user,"%%%%%%%%%%%%%%5access_user__________group_users",grp_users
        res_partner = request.registry.get('res.partner')
        new_partner_users = res_partner.search(cr, SUPERUSER_ID,[('email','=',post.get('email_from'))], context=context)
        print "ahi pura thaya==============>>>>>>>>>>>>",new_partner_users[0]
        for f in ['email_from', 'partner_name', 'description']:
            value[f] = post.get(f)
        for f in ['department_id', 'job_id']:
            value[f] = int(post.get(f) or 0)
        # Retro-compatibility for saas-3. "phone" field should be replace by "partner_phone" in the template in trunk.
        value['partner_phone'] = post.pop('phone', False)
        value['partner_id'] = new_partner_users[0] or False

        print "value['partner_id']000==============>>>>>>>>>>>>",value['partner_id']
        applicant_id = env['hr.applicant'].create(value).id
        if post['ufile']:
            attachment_value = {
                'name': post['ufile'].filename,
                'res_name': value['partner_name'],
                'res_model': 'hr.applicant',
                'res_id': applicant_id,
                'datas': base64.encodestring(post['ufile'].read()),
                'datas_fname': post['ufile'].filename,
            }
            env['ir.attachment'].create(attachment_value)
        return request.render("website_hr_recruitment_custom.thankyou", {})

# vim :et:
