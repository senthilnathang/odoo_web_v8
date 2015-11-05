# -*- coding: utf-8 -*-
##############################################################################
#
#
#    Copyright (C) 2015 Browseinfo SPRL (<http://Browseinfo.in>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, osv
from openerp.tools.translate import _


class survey_new_result(osv.Model):
    _inherit = "survey.user_input"

    def _func_result(self, cr, uid, ids, name, args, context=None):
        ret = {}
        print "uuuuuuuuuuuiiiiiidddddddddd======", uid
        res_users = self.pool.get("res.users")
        hr_req = self.pool.get("hr.recruitment.stage")
        hr_appl = self.pool.get("hr.applicant")
        for user_input in self.browse(cr, uid, ids, context=context):
            if user_input.quizz_score > 60:

                res_partners_id = res_users.browse(
                    cr, uid, uid, context=context).partner_id
                print "res_partners_id=============", res_partners_id.id
                hr_applicant_ids = hr_appl.search(
                    cr, uid, [('partner_id', '=', res_partners_id.id)],
                    context=context)
                print "hr_applicant_ids============", hr_applicant_ids
                hr_applicant_id = ''

                if isinstance(hr_applicant_ids, (list)):
                    hr_applicant_id = hr_applicant_ids[0]
                    print "hr_applicant_id==============>>>>", hr_applicant_id

                    hr_appl_id = hr_req.search(
                        cr, uid, [('name', '=', 'Second Interview')],
                        context=context)
                    stg_id = ''
                    if isinstance(hr_appl_id, (list)):
                        stg_id = hr_appl_id[0]
                        print "FFFFFfffffffffffiiinall_____id______", stg_id
                    grp_users = hr_appl.write(
                        cr, uid, hr_applicant_id,
                        {'stage_id': stg_id}, context)
                ret[user_input.id] = "Pass"

            else:

                res_partners_id = res_users.browse(cr, uid, uid,
                                                   context=context).partner_id
                print "res_partners_id=======>>>", res_partners_id.id
                hr_applicant_ids = hr_appl.search(cr, uid,
                                                  [('partner_id', '=',
                                                    res_partners_id.id)],
                                                  context=context)
                hr_applicant_id = ''

                if isinstance(hr_applicant_ids, (list)):
                    hr_applicant_id = hr_applicant_ids[0]
                    print "hr_applicant_id====>>>>", hr_applicant_id

                    hr_appl_id = hr_req.search(cr, uid,
                                               [('name', '=', 'Refused')],
                                               context=context)
                    print "iiddd---->>", hr_appl_id
                    if isinstance(hr_appl_id, (list)):
                        ids = hr_appl_id[0]
                    print "FFFFFfffffffffffiiinall_____id______", ids
                    grp_users = hr_appl.write(cr, uid, hr_applicant_id,
                                              {'stage_id': ids}, context)
                ret[user_input.id] = "Fail"
        return ret

    _columns = {
        'score_result': fields.function(_func_result,
                                        type="char", string="Result"),
    }

survey_new_result()


class hr_applicant(osv.Model):
    _inherit = 'hr.applicant'
    _columns = {
        'attachment': fields.binary("Attachment"),
        #'filedata': fields.binary('Texto',filters='*.xml'),
    }
hr_applicant()
