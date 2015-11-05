# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>)
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
import logging
import time
from datetime import datetime,date

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools import float_is_zero
from openerp.tools.translate import _
from openerp import tools, api, models
from openerp.addons.base.res.res_partner import format_address

import openerp.addons.decimal_precision as dp
import openerp.addons.product.product

class res_partner(osv.osv):
    _inherit = 'res.partner'
    
    def search(self, cr, user, args, offset=0, limit=None, order=None, context=None, count=False):
        args += [('dealer_or_partner','in', [False, ''])]
        return super(res_partner, self).search(cr, user, args, offset=offset, limit=limit, order=order,
            context=context, count=count)
    
    
    def _opportunity_meeting_phonecall_lead_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,{'opportunity_count': 0, 'meeting_count': 0}), ids))
        # the user may not have access rights for opportunities or meetings
        try:
            for partner in self.browse(cr, uid, ids, context):
                if partner.is_company:
                    operator = 'child_of'
                else:
                    operator = '='
                opp_ids = self.pool['crm.lead'].search(cr, uid, [('partner_id', operator, partner.id), ('type', '=', 'opportunity'), ('probability', '<', '100')], context=context)
                
                lead_ids = self.pool['crm.lead'].search(cr, uid, [('partner_id', operator, partner.id), ('type', '=', 'lead'), ('probability', '<', '100')], context=context)
                
                res[partner.id] = {
                    'opportunity_count': len(opp_ids),
                    'meeting_count': len(partner.meeting_ids),
                    'lead_count' : len(lead_ids),
                }
        except:
            pass
        for partner in self.browse(cr, uid, ids, context):
            res[partner.id]['phonecall_count'] = len(partner.phonecall_ids)
        return res

    def _sold_item_record(self, cr, uid, ids, field_name, arg, context=None):
        """Return the list of items sold by this partner"""
        res = {}
        Sale_order_pool = self.pool.get('sale.order')
        Stock_pick_pool = self.pool.get('stock.picking')
        item_list = []
        item_sold_dict = {}
        for partner in self.browse(cr, uid, ids, context=context):
            sale_ids = Sale_order_pool.search(cr, uid, [('partner_id', '=', partner.id), ('state', '=', 'done')])
            sale_objs = Sale_order_pool.browse(cr, uid, sale_ids)
            for sale_obj in sale_objs:
                stock_pick_ids = Stock_pick_pool.search(cr, uid, [('origin', '=', sale_obj.name), ('state', '=', 'done')])
                contract_id = sale_obj.project_id.id
                if stock_pick_ids:
                    stock_pick_objs = Stock_pick_pool.browse(cr, uid, stock_pick_ids)
                    for pack_id in stock_pick_objs[0].pack_operation_ids:
                        item_sold_dict = {
                            'product_id' :  pack_id.product_id.id,
                            'consign_date' : pack_id.date,
                            'serial_no' : pack_id.lot_id.id,
                            'consign_id' : pack_id.location_dest_id.id,
                            'contract_id' : contract_id,
                        }
                        print '\n irem sold dict++++++++++++',item_sold_dict
                        item_id = self.pool.get('item.sold').create(cr, uid, item_sold_dict)
                        item_list.append(item_id)
                        print '\n item list=================',item_list
            res[partner.id] = item_list
        return res
    
    
    _columns = {
        'last_name' : fields.char("Last Name", required=True),
        'first_name': fields.char('First Name'),
        'partner_last_name': fields.char('Last Name'),
        'partner_email': fields.char('Email'),
        'partner_function': fields.char('Job Title'),
        'personal_no' : fields.char('Personal No'),
        'marital_status': fields.selection(
                [('single', 'Single'), ('engaged', 'Engaged'), ('married', 'Married'), ('partners', 'Partners'), ('couple', 'Couple'), ('widower', 'Widower'), ('divorced', 'Divorced')],
                string='Marital Status', copy=False),
        'work_phone': fields.char('Work Phone'),
        'cell_phone': fields.char('Cell Phone'),
        'home_phone': fields.char('Home Phone'),
        'cust_home_phone_2': fields.char('Home Phone (2)'),
        'cust_mobile_phone_2': fields.char('Mobile Phone (2)'),
        'cust_work_phone': fields.char('Work Phone'),
        'cust_email_2': fields.char('Email (2)'),
        'cust_place_emp': fields.char('Place of Employment'),
        'children' : fields.boolean('Children'),
        'child_1': fields.char('Child 1'),
        'child_2': fields.char('Child 2'),
        'child_3': fields.char('Child 3'),
        'child_4': fields.char('Child 4'),
        'own_rent': fields.selection(
                [('own', 'Own'), ('rent', 'Rent')],
                string='Own or Rent?', copy=False),
        'partner_place_emp': fields.char('Place of Employment'),
        'partner_cell_phone': fields.char('Cell Phone'),
        'partner_home_phone': fields.char('Home Phone'),
        'partner_work_phone': fields.char('Work Phone'),
        'address_same_yes': fields.selection([('yes', 'Yes'), ('no', 'No')]),
        'street_2': fields.char('Street'),
        'street2_2': fields.char('Street2'),
        'city_2': fields.char('City'),
        'country_id_2': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'state_id_2': fields.many2one("res.country.state", 'State', ondelete='restrict'),
        'zip_2': fields.char('Zip', size=24, change_default=True),
        'cust_street_2': fields.char('Street'),
        'cust_street2_2': fields.char('Street2'),
        'cust_city_2': fields.char('City'),
        'cust_country_id_2': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'cust_state_id_2': fields.many2one("res.country.state", 'State', ondelete='restrict'),
        'cust_zip_2': fields.char('Zip', size=24, change_default=True),
        
        'appointment_type': fields.selection(
                [('owner', 'Owner')],
                'Appointment Type', copy=False),
        'referred_by': fields.many2one('res.partner', 'Referred By'),
        'lead_type': fields.many2one('crm.lead.type', 'Lead type'),
        'dealer': fields.many2one('res.dealer', 'Dealer'),
        'sponsor': fields.many2one('res.partner', 'Sponsor'),
        'event_source': fields.many2one('crm.tracking.source', string='Event'),
        'allergies_yes': fields.selection([('yes', 'Yes'), ('no', 'No')]),
        'pets_yes': fields.selection([('yes', 'Yes'), ('no', 'No')]),
        'comment_other': fields.text('Notes'),
        'company_owner': fields.boolean('Company Owner?'),
        'fiscal_id': fields.char('Fiscal ID'),
        'registry': fields.char('Registration Number'),
        
        'cust_company_name': fields.many2one('res.company', 'Company'),
        'company_id_1': fields.many2one('res.company', 'Company'),
        'company_id_2': fields.many2one('res.company', 'Company'),
        'comp1_title': fields.many2one('res.partner.title', 'Title'),
        'comp2_title': fields.many2one('res.partner.title', 'Title'),
        'company_acc_number': fields.char('Company BANK ACCOUNT'),
        'company_act_1': fields.text('Company Activity Domain'),
        'company_act_2': fields.text('Company Activity Domain'),
        'company_vat': fields.char('VAT NUMBER'),
        'comp1_fiscal_id': fields.char('Fiscal ID'),
        'comp1_registry': fields.char('Registration Number'),
        'comp2_fiscal_id': fields.char('Fiscal ID'),
        'comp2_registry': fields.char('Registration Number'),
        'comp1_street': fields.char('Street'),
        'comp1_street2': fields.char('Street2'),
        'comp1_country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'comp1_state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
        'comp1_zip': fields.char('ZIP', size=24, change_default=True),
        'comp1_city': fields.char('CITY'),

        'company_id_3': fields.many2one('res.company', 'Company'),
        'comp3_title': fields.many2one('res.partner.title', 'Title'),
        'company_act_3': fields.text('Company Activity Domain'),
        'comp3_fiscal_id': fields.char('Fiscal ID'),
        'comp3_registry': fields.char('Registration Number'),
        'comp3_street': fields.char('Street'),
        'comp3_street2': fields.char('Street2'),
        'comp3_country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'comp3_state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
        'comp3_zip': fields.char('ZIP', size=24, change_default=True),
        'comp3_city': fields.char('CITY'),
        
        'company_id_4': fields.many2one('res.company', 'Company'),
        'comp4_title': fields.many2one('res.partner.title', 'Title'),
        'company_act_4': fields.text('Company Activity Domain'),
        'comp4_fiscal_id': fields.char('Fiscal ID'),
        'comp4_registry': fields.char('Registration Number'),
        'comp4_street': fields.char('Street'),
        'comp4_street2': fields.char('Street2'),
        'comp4_country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'comp4_state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
        'comp4_zip': fields.char('ZIP', size=24, change_default=True),
        'comp4_city': fields.char('CITY'),
        
        'comp2_street': fields.char('Street'),
        'comp2_street2': fields.char('Street2'),
        'comp2_country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'comp2_state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
        'comp2_zip': fields.char('ZIP', size=24, change_default=True),
        'comp2_city': fields.char('CITY'),
        'meeting_count': fields.function(_opportunity_meeting_phonecall_lead_count, string="# Appointments", type='integer', multi='meeting_count'),
        'partner_leads' : fields.one2many('crm.lead', 'partner_id', string="Leads", readonly=True, ),
        'lead_count': fields.function(_opportunity_meeting_phonecall_lead_count, string="# Leads", type='integer', multi='meeting_count'),
        'active_campaign_ids' : fields.one2many('crm.campaign', 'partner_id', string="Active Campaigns", domain=[('days_left', '!=', 0)], readonly=True),
        'past_campaign_ids' : fields.one2many('crm.campaign', 'partner_id', string="Past Campaigns", domain=[('days_left', '=', 0)]),
        'customer_acc_inv' : fields.one2many('account.invoice', 'partner_id', string="Customer Invoice Info", readonly=True, domain=[('type', '=', 'out_invoice')]),
        'customer_payment' : fields.one2many('account.voucher', 'partner_id', string="Customer Payment Info", readonly=True, domain=[('type', '=', 'receipt')]),
        'call_history' : fields.one2many('crm.phonecall', 'partner_id', string="Logged Calls", readonly=True),
        'appointment_ids' : fields.one2many('calendar.event', 'partner_id', string="Appointments", readonly=True),
        'gift_ids': fields.one2many('gift.line', 'partner_id', 'Gifts', copy=False),
        'prod_warr_ids': fields.one2many('product.warranty', 'partner_warr_id', 'Warranty Revision', copy=False),
        'more_comp' : fields.boolean('More Companies?'),
        'prod_service_ids' : fields.one2many('product.warranty', 'partner_service_id', 'Service Revision', copy=False),
        
        'appt_type' : fields.many2one('appt.type', 'Appt Type'),
        'date_set' : fields.date('Date Set'),
        'date_sold' : fields.date('Date Sold'),
        'serial_no' : fields.many2one('stock.production.lot', 'Serial #'),
        'dealer_id': fields.many2one('res.dealer', 'Dealer'),
        'dealer_position' : fields.many2one('dealer.position', 'Position'),
        'advance_date' : fields.date('Advance Date'),
        'sale_amt' : fields.char('Sale'),
        'tax_rate' : fields.char('Tax Rate'),
        'total_tax' : fields.char('Total Tax'),
        'total_sale' : fields.char('Total Sale'),
        'sponsor_id_2': fields.many2one('res.partner', 'Sponsor'),
        'lead_dealer_id': fields.many2one('res.dealer', 'Lead Dealer'),
        'assistant_id' : fields.many2one('res.users', 'Assistant'),
        'ride_along_id' : fields.many2one('res.users', 'Ride-Along'),
        'set_by' : fields.many2one('res.users', 'Set By'),
        'prob_with_sale' : fields.many2one('sale.problem', 'Problem With Sale'),
        'sale_comment' : fields.text('Sale Comments'),
        
        'pay_type': fields.many2one('account.payment.term', 'Payment Type'),
        'option' : fields.char('Options'),
        'down_payment' : fields.char('Down Payment'),
        'down_type': fields.many2one('payment.type', 'Down Type'),
        'amount_financed' : fields.char('Amount Financed'),
        'filling_fee' : fields.char('Filling Fee'),
        'reserve_amt' : fields.char('Reserve Amount'),
        'discount_amt' : fields.char('Discount Amount'),
        'sac_disc' : fields.char('S.A.C Discount'),
        'balance_due' : fields.char('Balance Due'),
        'net_sale' : fields.char('Net Sale'),
        'comment_warranty' : fields.text('Notes'),
        'comment_service' : fields.text('Notes'),
        'sold_item_ids': fields.function(_sold_item_record, type="one2many", obj='item.sold', string="Item Sold"),
        
        'dealer_or_partner': fields.boolean('Dealer'),
    }

    def onchange_add(self, cr, uid, ids, address_same_yes, context=None):
        print '\n onchange of partner',ids,context
        result = {}
        partner_obj = self.browse(cr, uid, ids)
        if address_same_yes == 'yes':
            result['value'] = {'street_2': partner_obj.street, 'street2_2': partner_obj.street2, 'city_2' : partner_obj.city, 'country_id_2' : partner_obj.country_id, 'state_id_2' : partner_obj.state_id, 'zip_2' : partner_obj.zip}
        return result

    def onchange_dealer(self, cr, uid, ids, dealer, context=None):
        print '\n onchange of partner',ids,context,self,dealer
        result = {}
        Dealer_pool = self.pool.get('res.dealer')
        if dealer:
            dealer_obj = Dealer_pool.browse(cr, uid, dealer)
            result['value'] = {'sponsor' : dealer_obj.sponsor.id}
        print '\n onchange dealer',result
        return result

    def onchange_comp1(self, cr, uid, ids, company, context=None):
        result = {}
        company_obj = self.pool.get('res.company').browse(cr, uid, company)
        result['value'] = {'comp1_street': company_obj.street, 'comp1_street2': company_obj.street2,  'comp1_country_id': company_obj.country_id, 'comp1_state_id': company_obj.state_id, 'comp1_zip': company_obj.zip, 'comp1_city' : company_obj.city, 'comp1_registry' : company_obj.company_registry, 'company_id_1' : company}
        return result

    def onchange_comp2(self, cr, uid, ids, company, context=None):
        result = {}
        company_obj = self.pool.get('res.company').browse(cr, uid, company)
        result['value'] = {'comp2_street': company_obj.street, 'comp2_street2': company_obj.street2,  'comp2_country_id': company_obj.country_id, 'comp2_state_id': company_obj.state_id, 'comp2_zip': company_obj.zip, 'comp2_city' : company_obj.city, 'comp2_vat' : company_obj.vat, 'comp2_registry' : company_obj.company_registry}
        return result

    def onchange_comp3(self, cr, uid, ids, company, context=None):
        result = {}
        company_obj = self.pool.get('res.company').browse(cr, uid, company)
        result['value'] = {'comp3_street': company_obj.street, 'comp3_street2': company_obj.street2,  'comp3_country_id': company_obj.country_id, 'comp3_state_id': company_obj.state_id, 'comp3_zip': company_obj.zip, 'comp3_city' : company_obj.city, 'comp3_vat' : company_obj.vat, 'comp3_registry' : company_obj.company_registry}
        return result

    def onchange_comp4(self, cr, uid, ids, company, context=None):
        result = {}
        company_obj = self.pool.get('res.company').browse(cr, uid, company)
        result['value'] = {'comp4_street': company_obj.street, 'comp4_street2': company_obj.street2,  'comp4_country_id': company_obj.country_id, 'comp4_state_id': company_obj.state_id, 'comp4_zip': company_obj.zip, 'comp4_city' : company_obj.city, 'comp4_vat' : company_obj.vat, 'comp4_registry' : company_obj.company_registry}
        return result

class res_dealer(osv.Model):
    _name = 'res.dealer'

    @api.multi
    def _get_image(self, name, args):
        return dict((p.id, tools.image_get_resized_images(p.image)) for p in self)

    @api.one
    def _set_image(self, name, value, args):
        return self.write({'image': tools.image_resize_image_big(value)})

    def onchange_add(self, cr, uid, ids, address_same_yes, context=None):
        result = {}
        partner_obj = self.browse(cr, uid, ids)
        if address_same_yes == 'yes':
            result['value'] = {'street_2': partner_obj.street, 'street2_2': partner_obj.street2, 'city_2' : partner_obj.city, 'country_id_2' : partner_obj.country_id, 'state_id_2' : partner_obj.state_id, 'zip_2' : partner_obj.zip}
        return result

    def onchange_comp2(self, cr, uid, ids, company, context=None):
        result = {}
        company_obj = self.pool.get('res.company').browse(cr, uid, company)
        result['value'] = {'comp2_street': company_obj.street, 'comp2_street2': company_obj.street2,  'comp2_country_id': company_obj.country_id, 'comp2_state_id': company_obj.state_id, 'comp2_zip': company_obj.zip, 'comp2_city' : company_obj.city, 'comp2_vat' : company_obj.vat, 'comp2_registry' : company_obj.company_registry}
        return result

    def onchange_comp3(self, cr, uid, ids, company, context=None):
        result = {}
        company_obj = self.pool.get('res.company').browse(cr, uid, company)
        result['value'] = {'comp3_street': company_obj.street, 'comp3_street2': company_obj.street2,  'comp3_country_id': company_obj.country_id, 'comp3_state_id': company_obj.state_id, 'comp3_zip': company_obj.zip, 'comp3_city' : company_obj.city, 'comp3_vat' : company_obj.vat, 'comp3_registry' : company_obj.company_registry}
        return result

    def onchange_comp4(self, cr, uid, ids, company, context=None):
        result = {}
        company_obj = self.pool.get('res.company').browse(cr, uid, company)
        result['value'] = {'comp4_street': company_obj.street, 'comp4_street2': company_obj.street2,  'comp4_country_id': company_obj.country_id, 'comp4_state_id': company_obj.state_id, 'comp4_zip': company_obj.zip, 'comp4_city' : company_obj.city, 'comp4_vat' : company_obj.vat, 'comp4_registry' : company_obj.company_registry}
        return result

    def onchange_comp1(self, cr, uid, ids, company, context=None):
        result = {}
        company_obj = self.pool.get('res.company').browse(cr, uid, company)
        result['value'] = {'comp1_street': company_obj.street, 'comp1_street2': company_obj.street2,  'comp1_country_id': company_obj.country_id, 'comp1_state_id': company_obj.state_id, 'comp1_zip': company_obj.zip, 'comp1_city' : company_obj.city, 'comp1_registry' : company_obj.company_registry, 'company_id_1' : company}
        return result
        
    def _appointment_trips_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,{'appointment_count': 0, 'trips_count': 0, 'demos_count' : 0, 'contest_count' : 0, 'sales_count' : 0, 'total_income' : 0}), ids))
        # the user may not have access rights for opportunities or meetings
        try:
            for dealer in self.browse(cr, uid, ids, context):
                appot_ids = self.pool['calendar.event'].search(cr, uid, [('dealer_id', '=', dealer.id)], context=context)
                
                trips_ids = self.pool['calendar.event'].search(cr, uid, [('dealer_id', '=', dealer.id), ('meeting_type', '=', 'trips')], context=context)
                
                demo_ids = self.pool['crm.lead'].search(cr, uid, [('dealer_id', '=', dealer.id), ('stage_id', '=', 'Won')])
                sale_ids = self.pool['sale.order'].search(cr, uid, [('dealer_id', '=', dealer.id), ('state', '=', 'done')])
                if sale_ids:
                    total_income = 0
                    amount_dicts = self.pool['sale.order'].read(cr, uid, sale_ids, ['amount_total'])
                    for amount_dict in amount_dicts:
                        total_income += amount_dict.get('amount_total')
                        print '\n total income',total_income
                        
                contest_ids = self.pool['crm.contest'].search(cr, uid, [('dealer_id', '=', dealer.id), ('campaign_success', '=', 'yes')])
                res[dealer.id] = {
                    'appointment_count': len(appot_ids),
                    'trips_count': len(trips_ids),
                    'demos_count' : len(demo_ids),
                    'contest_count' : len(contest_ids),
                    'sales_count' : len(sale_ids),
                    'total_income' : total_income,
                }
        except:
            pass
        return res
        
        
    def _consigned_product_record(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        Sale_order_pool = self.pool.get('sale.order')
        Stock_pick_pool = self.pool.get('stock.picking')
        item_list = []
        prod_consign_dict = {}
        for dealer in self.browse(cr, uid, ids, context=context):
            sale_ids = Sale_order_pool.search(cr, uid, [('dealer_id', '=', dealer.id), ('state', '=', 'done')])
            sale_objs = Sale_order_pool.browse(cr, uid, sale_ids)
            for sale_obj in sale_objs:
                stock_pick_ids = Stock_pick_pool.search(cr, uid, [('origin', '=', sale_obj.name), ('state', '=', 'done')])
                if stock_pick_ids:
                    stock_pick_objs = Stock_pick_pool.browse(cr, uid, stock_pick_ids)
                    partner_id = stock_pick_objs[0].partner_id
                    print '\n in consigned ids',stock_pick_objs[0].picking_type_id,stock_pick_objs[0].picking_type_id.code
                    for pack_id in stock_pick_objs[0].pack_operation_ids:
                        prod_consign_dict = {
                            'product_id' :  pack_id.product_id.id,
                            'consign_date' :  stock_pick_objs[0].picking_type_id.code == 'outgoing' and stock_pick_objs[0].date_done,
                            'serial_no' : pack_id.lot_id.id,
#                            'return_date' : stock_pick_objs[0].date_done,
                            'partner_id' : partner_id.id,
                        }
                        print '\n irem sold dict++++++++++++',prod_consign_dict
                        item_id = self.pool.get('product.consignment').create(cr, uid, prod_consign_dict)
                        item_list.append(item_id)
                        print '\n item list=================',item_list
            res[dealer.id] = item_list
        return res
        
        
    _columns = {
        'name': fields.char('Name', required=True),
        'last_name': fields.char('Last Name', required=True),
        'fname': fields.char('Name'),
        'lname': fields.char('Last Name'),
        'dealer_name': fields.char('Dealer Name'),
        'personal_no' : fields.char('Personal No'),
        'marital_status': fields.selection(
                [('single', 'Single'), ('engaged', 'Engaged'), ('married', 'Married'), ('partners', 'Partners'), ('couple', 'Couple'), ('widower', 'Widower'), ('divorced', 'Divorced')],
                string='Marital Status', copy=False),
        'spouse': fields.char('Spouse'),
        'code': fields.char('Code'),
        'home_phone': fields.char('Home Phone'),
        'home_phone2': fields.char('Home Phone (2)'),
        'work_phone': fields.char('Work Phone'),
        'work_phone2': fields.char('Work Phone (2)'),
        'address': fields.char('Address1'),
        'street': fields.char('Street'),
        'street2': fields.char('Street2'),
        'city': fields.char('City'),
        'country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
        'zip': fields.char('Zip', size=24, change_default=True),
        'company_owners': fields.boolean('Company Owner?'),
        'cust_company_name': fields.many2one('res.company', 'Company'),
        'partner_name': fields.char('Partner Name'),
        'section_id': fields.many2one('crm.case.section', 'Sales Team'),
        'manager_name': fields.many2one('res.users', 'Manager Name'),
        'manager': fields.many2one('res.users', 'Manager'),
        'organization': fields.char('Organization'),
        'partner_company_name': fields.many2one('res.company', 'Company'),
        'start_date': fields.date('Start Date'),
        'graduation_date': fields.date('Graduation Date'),
        'elig_for_override': fields.date('Eligible For Overrides'),
        'sponsored_by': fields.many2one('res.partner', 'Sponsored By'),
        'comp_title': fields.many2one('res.partner.title', 'Title'),
        'position': fields.many2one('dealer.position', 'Position', copy=False),
        'full_time': fields.boolean('Full Time'),
        'part_time': fields.boolean('Part Time'),
        'branch': fields.char('Branch'),
        'comment': fields.text('Comment'),
        'comp2_fiscal_id': fields.char('Fiscal ID'),
        'comp2_country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'organization': fields.char('Organization'),
        'lead_type': fields.many2one('crm.lead.type', 'Lead type'),
        'company_owner': fields.boolean('Company Owner?'),
        'company_name': fields.many2one('res.company', 'Company'),
        'responsible_user_id': fields.many2one('res.users', 'Responsible As Manager For'),
        'image': fields.binary("Image",
            help="This field holds the image used as avatar for this contact, limited to 1024x1024px"),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store={
                'res.dealer': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized image of this contact. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),
        'allergies_yes': fields.selection([('yes', 'Yes'), ('no', 'No')]),
        'pets_yes': fields.selection([('yes', 'Yes'), ('no', 'No')]),
        'comment_other': fields.text('Notes'),
        'partner_cell_phone': fields.char('Cell Phone'),
        'address_same_yes': fields.selection([('yes', 'Yes'), ('no', 'No')]),
        'work_as_team': fields.boolean('Working as TEAM?'),
        'team_name': fields.many2one('crm.case.section', 'Team Name'),
        'children': fields.boolean('Children(s)'),
        'child_1': fields.char('Child 1'),
        'child_2': fields.char('Child 2'),
        'child_3': fields.char('Child 3'),
        'child_4': fields.char('Child 4'),
        'dealer': fields.many2one('res.dealer', 'Dealer'),
        'sponsor': fields.many2one('res.partner', 'Sponsor'),
        'partner_home_phone': fields.char('Home Phone'),
        'partner_work_phone': fields.char('Work Phone'),
        'event_source': fields.many2one('crm.tracking.source', string='Event'),
        'partner_email': fields.char('Email'),
        'street2_2': fields.char('Street2'),
        'street_2': fields.char('Street'),
        'country_id_2': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'referred_by': fields.many2one('res.partner', 'Referred By'),
        'city_2': fields.char('City'),
        'zip_2': fields.char('Zip', size=24, change_default=True),
        'company_owner': fields.boolean('Company Owner?'),
        'cust_company_name': fields.many2one('res.company', 'Company'),
        'company_id_1': fields.many2one('res.company', 'Company'),
        'company_id_2': fields.many2one('res.company', 'Company'),
        'comp1_title': fields.many2one('res.partner.title', 'Title'),
        'comp2_title': fields.many2one('res.partner.title', 'Title'),
        'company_acc_number': fields.char('Company BANK ACCOUNT'),
        'company_act_1': fields.text('Company Activity Domain'),
        'company_act_2': fields.text('Company Activity Domain'),
        'company_vat': fields.char('VAT NUMBER'),
        'comp1_fiscal_id': fields.char('Fiscal ID'),
        'comp1_registry': fields.char('Registration Number'),
        'comp2_fiscal_id': fields.char('Fiscal ID'),
        'comp2_registry': fields.char('Registration Number'),
        'comp1_street': fields.char('Street'),
        'comp1_street2': fields.char('Street2'),
        'comp1_country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'comp1_state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
        'comp1_zip': fields.char('ZIP', size=24, change_default=True),
        'comp1_city': fields.char('CITY'),
        'state_id_2': fields.many2one("res.country.state", 'State', ondelete='restrict'),
        'comp2_street': fields.char('Street'),
        'comp2_street2': fields.char('Street2'),
        'comp2_country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'comp2_state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
        'comp2_zip': fields.char('ZIP', size=24, change_default=True),
        'comp2_city': fields.char('CITY'),

        'more_comp' : fields.boolean('More Companies?'),
        'company_id_3': fields.many2one('res.company', 'Company'),
        'comp3_title': fields.many2one('res.partner.title', 'Title'),
        'company_act_3': fields.text('Company Activity Domain'),
        'comp3_fiscal_id': fields.char('Fiscal ID'),
        'comp3_registry': fields.char('Registration Number'),
        'comp3_street': fields.char('Street'),
        'comp3_street2': fields.char('Street2'),
        'comp3_country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'comp3_state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
        'comp3_zip': fields.char('ZIP', size=24, change_default=True),
        'comp3_city': fields.char('CITY'),
        'company_id_4': fields.many2one('res.company', 'Company'),
        'comp4_title': fields.many2one('res.partner.title', 'Title'),
        'company_act_4': fields.text('Company Activity Domain'),
        'comp4_fiscal_id': fields.char('Fiscal ID'),
        'comp4_registry': fields.char('Registration Number'),
        'comp4_street': fields.char('Street'),
        'comp4_street2': fields.char('Street2'),
        'comp4_country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'comp4_state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
        'comp4_zip': fields.char('ZIP', size=24, change_default=True),
        'comp4_city': fields.char('CITY'),

        'partner_leads' : fields.one2many('crm.lead', 'dealer', string="Leads", readonly=True, ),
        'active_contest_ids' : fields.one2many('crm.contest', 'dealer_id', string="Active Contest", domain=[('days_left', '!=', 0)], readonly=True),
        'past_contest_ids' : fields.one2many('crm.contest', 'dealer_id', string="Past Contest", domain=[('days_left', '=', 0)]),
        
        'partner_sale_info' : fields.one2many('sale.order', 'dealer_id', string="Sales Info", readonly=True),
        'customer_acc_inv' : fields.one2many('account.invoice', 'dealer_id', string="Customer Invoice Info", readonly=True, domain=[('type', '=', 'out_invoice')]),
        'consignment_ids': fields.function(_consigned_product_record, type="one2many", obj='product.consignment', string="CONSIGNMENTS"),
        'customer_payment' : fields.one2many('account.voucher', 'dealer_id', string="Customer Payment Info", readonly=True, domain=[('type', '=', 'receipt')]),
        'future_meetings' : fields.one2many('calendar.event', 'dealer_id', string="Future Meetings", readonly=True, domain=[('meeting_type', '=', 'normal'), ('start_datetime','>',time.strftime('%m/%d/%Y %H:%M:%S'))]),
        'past_meetings' : fields.one2many('calendar.event', 'dealer_id', string="Past Events", readonly=True, domain=[('meeting_type', '=', 'normal'), ('start_datetime','<',time.strftime('%m/%d/%Y %H:%M:%S'))]),
        'appointment_ids' : fields.one2many('calendar.event', 'dealer_id', string="Appointments", readonly=True),
        'trip_meetings' : fields.one2many('calendar.event', 'dealer_id', string="Trips", readonly=True, domain=[('meeting_type', '=', 'trips')]),
        'gift_ids': fields.one2many('gift.line', 'dealer_id', 'Gifts', copy=False),
        'appointment_type': fields.selection(
                [('owner', 'Owner')],
                'Appointment Type', copy=False),
        'commission_ids' : fields.one2many('sale.order', 'dealer_id', string="COMMISSIONS", readonly=True),
        
        'appointment_count' : fields.function(_appointment_trips_count, type="char", string='Appointments', multi="appointment_count"),
        'trips_count' : fields.function(_appointment_trips_count, type="char", string='Trips', multi="appointment_count"),
        'demos_count' : fields.function(_appointment_trips_count, type="char", string='Demos Completed', multi="appointment_count"),
        'contest_count' : fields.function(_appointment_trips_count, type="char", string='Contests Won', multi="appointment_count"),
        'sales_count' : fields.function(_appointment_trips_count, type="char", string='Sales', multi="appointment_count"),
        'total_income' : fields.function(_appointment_trips_count, type="float", string='Total Income', multi="appointment_count"),

    }

    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {}

AVAILABLE_PRIORITIES = [
    ('0', 'Very Low'),
    ('1', 'Low'),
    ('2', 'Normal'),
    ('3', 'High'),
    ('4', 'Very High'),
]


class crm_lead(format_address, osv.osv):
    """ CRM Lead Case """
    _inherit = "crm.lead"
    def _get_stage_id(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if ids:
            for lead in self.browse(cr, uid, ids):
                res[lead.id] = lead.stage_id.name
        print '\n get stage id',res
        return res
        
    def name_get(self, cr, uid, ids, context=None):
        res = []
        print '\n name get of crm lead',self,context,res
        if (context and context.get('default_type') == 'lead') or (context and context.get('stage_type') == 'lead'):
            if not len(ids):
                return []
            for r in self.read(cr, uid, ids, ['name', 'last_name'], context=context):
                print '\n in if condi of name get ',r
                res.append((r['id'], '%s %s' %(r['name'], r['last_name'])))
                print 'r ilist of  name get of lead',res
            return res 
        elif (context and context.get('default_type') == 'opportunity') or (context and context.get('stage_type') == 'opportunity'):
            for r in self.read(cr, uid, ids, ['name'], context=context):
                print '\n in else condi of name get ',r
                res.append((r['id'], '%s' %(r['name'])))
                print 'r i name get of opportunities',res
            return res 
        else:
            return super(crm_lead, self).name_get(cr, uid, ids, context=context)
            
        
#    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
#        args = args or []
#        print '\n in name search',name,args,context
#        if name:
#            ids = self.search(cr, uid, [('code', '=', name)] + args, limit=limit, context=context or {})
#            if not ids:
#                ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context or {})
#        else:
#            ids = self.search(cr, uid, args, limit=limit, context=context or {})
#        return self.name_get(cr, uid, ids, context or {})

    _columns = {
            'priority': fields.selection(AVAILABLE_PRIORITIES, 'Priority', select=True),
            'name': fields.char('Name', select=1, readonly=False),
            'last_name': fields.char('Name', select=1, readonly=False),
            'partner_title': fields.many2one('res.partner.title', 'Title'),
            'company_owner': fields.boolean('Company Owner?'),
            'company_name': fields.many2one('res.company', 'Company'),
            'home_phone' : fields.char('Home Phone (2)'),
            'mobile_phone' : fields.char('Mobile Phone (2)'),
            'work_phone' : fields.char('Work Phone'),
            'email_2' : fields.char('Email (2)'),
            'place_emp': fields.char('Place of Employment'),
            'job_title': fields.char('Job Title'),
            'marital_status': fields.selection(
                [('single', 'Single'), ('engaged', 'Engaged'), ('married', 'Married'), ('partners', 'Partners'), ('couple', 'Couple'), ('widower', 'Widower'), ('divorced', 'Divorced')],
                string='Marital Status', copy=False),
            'personal_no' : fields.char('Personal No'),
            'street_2': fields.char('Street'),
            'street2_2': fields.char('Street2'),
            'city_2': fields.char('City'),
            'country_id_2': fields.many2one('res.country', 'Country', ondelete='restrict'),
            'state_id_2': fields.many2one("res.country.state", 'State', ondelete='restrict'),
            'zip_2': fields.char('Zip', size=24, change_default=True),
            'image': fields.binary("Image",
                help="This field holds the image used as avatar for this contact, limited to 1024x1024px"),
            'source_id' : fields.many2one('crm.tracking.source', string="Lead Source"),
            'dealer_id' : fields.many2one('res.dealer', string="Dealer"),
            'lead_type': fields.many2one('crm.lead.type', 'Lead type'),
            'own_rent': fields.selection(
                    [('own', 'Own'), ('rent', 'Rent')],
                    string='Own or Rent?', copy=False),
            'more_comp' : fields.boolean('More Companies?'),
                    
            'partner_first_name': fields.char('First Name'),
            'partner_last_name': fields.char('Last Name'),
            'partner_email': fields.char('Email'),
            'partner_function': fields.char('Job Title'),
            'partner_place_emp': fields.char('Place of Employment'),
            'partner_cell_phone': fields.char('Cell Phone'),
            'partner_home_phone': fields.char('Home Phone'),
            'partner_work_phone': fields.char('Work Phone'),
            'allergies_yes': fields.selection([('yes', 'Yes'), ('no', 'No')]),
            'pets_yes': fields.selection([('yes', 'Yes'), ('no', 'No')]),

            'children' : fields.boolean('Children'),
            'child_1': fields.char('Child 1'),
            'child_2': fields.char('Child 2'),
            'child_3': fields.char('Child 3'),
            'child_4': fields.char('Child 4'),
            'appointment_type': fields.selection(
                    [('owner', 'Owner')],
                    'Appointment Type', copy=False),
            'referred_by': fields.many2one('res.partner', 'Referred By'),
            'lead_type': fields.many2one('crm.lead.type', 'Lead type'),
            'dealer': fields.many2one('res.dealer', 'Dealer'),
            'sponsor': fields.many2one('res.partner', 'Sponsor'),
            'event_source': fields.many2one('crm.tracking.source', string='Event'),
            'comment_other': fields.text('Notes'),
            'comment': fields.text('Notes'),                    
            
            'company_id_1': fields.many2one('res.company', 'Company'),
            'comp1_title': fields.many2one('res.partner.title', 'Title'),
            'company_act_1': fields.text('Company Activity Domain'),
            'comp1_fiscal_id': fields.char('Fiscal ID'),
            'comp1_registry': fields.char('Registration Number'),
            'comp1_street': fields.char('Street'),
            'comp1_street2': fields.char('Street2'),
            'comp1_country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
            'comp1_state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
            'comp1_zip': fields.char('ZIP', size=24, change_default=True),
            'comp1_city': fields.char('CITY'),
            
            'company_id_2': fields.many2one('res.company', 'Company'),
            'comp2_title': fields.many2one('res.partner.title', 'Title'),
            'company_act_2': fields.text('Company Activity Domain'),
            'comp2_fiscal_id': fields.char('Fiscal ID'),
            'comp2_registry': fields.char('Registration Number'),
            'comp2_street': fields.char('Street'),
            'comp2_street2': fields.char('Street2'),
            'comp2_country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
            'comp2_state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
            'comp2_zip': fields.char('ZIP', size=24, change_default=True),
            'comp2_city': fields.char('CITY'),

            'company_id_3': fields.many2one('res.company', 'Company'),
            'comp3_title': fields.many2one('res.partner.title', 'Title'),
            'company_act_3': fields.text('Company Activity Domain'),
            'comp3_fiscal_id': fields.char('Fiscal ID'),
            'comp3_registry': fields.char('Registration Number'),
            'comp3_street': fields.char('Street'),
            'comp3_street2': fields.char('Street2'),
            'comp3_country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
            'comp3_state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
            'comp3_zip': fields.char('ZIP', size=24, change_default=True),
            'comp3_city': fields.char('CITY'),
            
            'company_id_4': fields.many2one('res.company', 'Company'),
            'comp4_title': fields.many2one('res.partner.title', 'Title'),
            'company_act_4': fields.text('Company Activity Domain'),
            'comp4_fiscal_id': fields.char('Fiscal ID'),
            'comp4_registry': fields.char('Registration Number'),
            'comp4_street': fields.char('Street'),
            'comp4_street2': fields.char('Street2'),
            'comp4_country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
            'comp4_state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
            'comp4_zip': fields.char('ZIP', size=24, change_default=True),
            'comp4_city': fields.char('CITY'),
            
            'address_same_yes': fields.selection([('yes', 'Yes'), ('no', 'No')]),
            'street_2': fields.char('Street'),
            'street2_2': fields.char('Street2'),
            'city_2': fields.char('City'),
            'country_id_2': fields.many2one('res.country', 'Country', ondelete='restrict'),
            'state_id_2': fields.many2one("res.country.state", 'State', ondelete='restrict'),
            'zip_2': fields.char('Zip', size=24, change_default=True),
            'result_id' : fields.many2one('appointment.result', 'Result'),
            
#            'lead_id' : fields.many2one('crm.lead', 'Leads'),
            
            'appt_type' : fields.many2one('appt.type', 'Appt Type'),
            'date_set' : fields.date('Date Set'),
            'date_sold' : fields.date('Date Sold'),
            'serial_no' : fields.many2one('stock.production.lot', 'Serial #'),
            'dealer_id': fields.many2one('res.dealer', 'Dealer'),
            'dealer_position' : fields.many2one('dealer.position', 'Position'),
            'advance_date' : fields.date('Advance Date'),
            'sale_amt' : fields.char('Sale'),
            'tax_rate' : fields.char('Tax Rate'),
            'total_tax' : fields.char('Total Tax'),
            'total_sale' : fields.char('Total Sale'),
            'sponsor_id_2': fields.many2one('res.partner', 'Sponsor'),
            'lead_dealer_id': fields.many2one('res.dealer', 'Lead Dealer'),
            'assistant_id' : fields.many2one('res.users', 'Assistant'),
            'ride_along_id' : fields.many2one('res.users', 'Ride-Along'),
            'set_by' : fields.many2one('res.users', 'Set By'),
            'prob_with_sale' : fields.many2one('sale.problem', 'Problem With Sale'),
            'sale_comment' : fields.text('Sale Comments'),
            
            'pay_type': fields.many2one('account.payment.term', 'Payment Type'),
            'option' : fields.char('Options'),
            'down_payment' : fields.char('Down Payment'),
            'down_type': fields.many2one('payment.type', 'Down Type'),
            'amount_financed' : fields.char('Amount Financed'),
            'filling_fee' : fields.char('Filling Fee'),
            'reserve_amt' : fields.char('Reserve Amount'),
            'discount_amt' : fields.char('Discount Amount'),
            'sac_disc' : fields.char('S.A.C Discount'),
            'balance_due' : fields.char('Balance Due'),
            'net_sale' : fields.char('Net Sale'),
            'comment_warranty' : fields.text('Notes'),
            'comment_service' : fields.text('Notes'),
            
            
#            'leads_ids' : fields.one2many('crm.lead', 'lead_id', string="Leads", readonly=True, ),
            'appointment_ids' : fields.one2many('calendar.event', 'lead_id', string="Appointments", readonly=True),
            'active_campaign_ids' : fields.one2many('crm.campaign', 'lead_id', string="Campaigns", domain=[('days_left', '!=', 0)]),
            'past_campaign_ids' : fields.one2many('crm.campaign', 'lead_id', string="Campaigns", domain=[('days_left', '=', 0)]),
            'call_history_ids' : fields.one2many('crm.phonecall', 'opportunity_id', string="Logged Calls", readonly=True),
            'gift_ids': fields.one2many('gift.line', 'lead_id', 'Gifts', copy=False),
            'customer_acc_inv' : fields.one2many('account.invoice', 'lead_id', string="Customer Invoice Info", readonly=True, domain=[('type', '=', 'out_invoice')]),
            'customer_payment' : fields.one2many('account.voucher', 'lead_id', string="Customer Payment Info", readonly=True, domain=[('type', '=', 'receipt')]),
            'prod_warr_ids': fields.one2many('product.warranty', 'lead_warr_id', 'Warranty Revision', copy=False),
            'prod_service_ids' : fields.one2many('product.warranty', 'lead_service_id', 'Service Revision', copy=False),
            'lead_type_button' : fields.char('Lead Type'),
            'next_action' : fields.date('Next Action'),
            'button_stage': fields.function(_get_stage_id,
            type="char", readonly=True, string='Stage'),
            'km': fields.char('KM'),
    }
    
#    _defaults = {
#        'name': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'crm.demo'),
#    }
    
    
#    def on_change_partner_id(self, cr, uid, ids, partner_id, context=None):
#        values = {}
#        if partner_id:
#            partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
#            values = {
#                'street': partner.street,
#                'street2': partner.street2,
#                'city': partner.city,
#                'state_id': partner.state_id and partner.state_id.id or False,
#                'country_id': partner.country_id and partner.country_id.id or False,
#                'zip': partner.zip,
#            }
#        return {'value': values}
        
    def show_google_map(self, cr, uid, ids, context):
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'crm_lead_extended', 'view_crm_lead_map')
        view_id = view_ref and view_ref[1] or False,
        return {
        'type': 'ir.actions.act_window',
        'name': 'Crm Lead',
        'res_model': 'crm.lead',
        'res_id': ids[0],
        'view_id': view_id,
        'view_type': 'form',
        'view_mode': 'form',
        'target': 'new',
        'nodestroy': True,
        }

    def onchange_lead_type(self, cr, uid, ids, lead_type, context=None):
        values = {}
        print '\n lead type ',ids,lead_type,context
        if lead_type:
            lead_type = self.pool.get('crm.lead.type').browse(cr, uid, lead_type).name
            values = {
                'lead_type_button': lead_type,
            }
        return {'value': values}
    
    def onchange_add(self, cr, uid, ids, address_same_yes, context=None):
        result = {}
        partner_obj = self.browse(cr, uid, ids)
        if address_same_yes == 'yes':
            result['value'] = {'street_2': partner_obj.street, 'street2_2': partner_obj.street2, 'city_2' : partner_obj.city, 'country_id_2' : partner_obj.country_id, 'state_id_2' : partner_obj.state_id, 'zip_2' : partner_obj.zip}
        return result

    def onchange_comp1(self, cr, uid, ids, company, context=None):
        result = {}
        company_obj = self.pool.get('res.company').browse(cr, uid, company)
        result['value'] = {'comp1_street': company_obj.street, 'comp1_street2': company_obj.street2,  'comp1_country_id': company_obj.country_id, 'comp1_state_id': company_obj.state_id, 'comp1_zip': company_obj.zip, 'comp1_city' : company_obj.city, 'comp1_registry' : company_obj.company_registry, 'company_id_1' : company, 'lead_type1' : company_obj.city}
        return result

    def onchange_comp2(self, cr, uid, ids, company, context=None):
        result = {}
        company_obj = self.pool.get('res.company').browse(cr, uid, company)
        result['value'] = {'comp2_street': company_obj.street, 'comp2_street2': company_obj.street2,  'comp2_country_id': company_obj.country_id, 'comp2_state_id': company_obj.state_id, 'comp2_zip': company_obj.zip, 'comp2_city' : company_obj.city, 'comp2_registry' : company_obj.company_registry}
        return result
    
    def onchange_comp3(self, cr, uid, ids, company, context=None):
        result = {}
        company_obj = self.pool.get('res.company').browse(cr, uid, company)
        result['value'] = {'comp3_street': company_obj.street, 'comp3_street2': company_obj.street2,  'comp3_country_id': company_obj.country_id, 'comp3_state_id': company_obj.state_id, 'comp3_zip': company_obj.zip, 'comp3_city' : company_obj.city, 'comp3_vat' : company_obj.vat, 'comp3_registry' : company_obj.company_registry}
        return result

    def onchange_comp4(self, cr, uid, ids, company, context=None):
        result = {}
        company_obj = self.pool.get('res.company').browse(cr, uid, company)
        result['value'] = {'comp4_street': company_obj.street, 'comp4_street2': company_obj.street2,  'comp4_country_id': company_obj.country_id, 'comp4_state_id': company_obj.state_id, 'comp4_zip': company_obj.zip, 'comp4_city' : company_obj.city, 'comp4_vat' : company_obj.vat, 'comp4_registry' : company_obj.company_registry}
        return result
    
    
    def action_schedule_meeting(self, cr, uid, ids, context=None):
        return super(crm_lead, self).action_schedule_meeting(cr, uid, ids, context=context)
    
    def onchange_dealer(self, cr, uid, ids, dealer, context=None):
        print '\n onchange of partner',ids,context,self,dealer
        result = {}
        Dealer_pool = self.pool.get('res.dealer')
        if dealer:
            dealer_obj = Dealer_pool.browse(cr, uid, dealer)
            result['value'] = {'sponsor' : dealer_obj.sponsor.id}
        print '\n onchange dealer',result
        return result
    
    

class crm_tracking_campaign(osv.Model):
    # OLD crm.case.resource.type
    _inherit = "crm.tracking.campaign"
    
    _columns = {
            'partner_id' : fields.many2one('res.partner', 'Partner'),
            'lead_id' : fields.many2one('crm.lead', 'Lead'),
            'dealer_id' : fields.many2one('res.dealer', 'Dealer'),
    }

class product_product(osv.osv):
    _inherit = "product.product"
    
    _columns = {
            'prod_gift' : fields.boolean('Gift'),
    }

class calendar_event(osv.Model):
    """ Model for Calendar Event """
    _inherit = 'calendar.event'
    _columns = {
            'image': fields.binary("Image",
            help="This field holds the image used as avatar for this contact, limited to 1024x1024px"),
            'first_name': fields.char('Name', required=True, select=1, readonly=False),
            'last_name': fields.char('Name', required=True, select=1, readonly=False),
            'street': fields.char('Street'),
            'street2': fields.char('Street2'),
            'partner_ids': fields.many2many('res.partner', 'calendar_event_res_partner_rel', string='Attendees', states={'done': [('readonly', True)]}),
            'city': fields.char('City'),
            'country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
            'state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
            'zip': fields.char('Zip', size=24, change_default=True),
            'meeting_type': fields.selection([('normal', 'Normal'), ('trips', 'Trips')],string='Meeting Type'),
            
            'user_id': fields.many2one('res.users', 'Responsible', states={'done': [('readonly', True)]}),
            'partner_id' : fields.many2one('res.partner', 'Partner'),
            'dealer_id' : fields.many2one('res.dealer', 'Dealer Assigned'),
            'supervisor_id' : fields.many2one('res.users', 'Supervisor'),
            'assistant_id' : fields.many2one('res.users', 'Assistant'),
            'operator_id' : fields.many2one('res.users', 'Operator'),
            'ride_along_id_1' : fields.many2one('res.users', 'Ride-Along'),
            'phone' : fields.char('Phone Number'),
            'name': fields.char('Subject', readonly=True, required=False),
            
            'result_id' : fields.many2one('appointment.result', 'Result'),
            'sale_amount' : fields.char('Amount of Sale'),
            'tracking_no' : fields.char('Tracking Number'),
            'leads_count' : fields.char('Number of Leads'),
            'assistant_id_2' : fields.many2one('res.users', 'Assistant'),
            'deliver_id' : fields.many2one('item.deliver', 'Delivered'),
            'allday': fields.boolean('All Day', states={'done': [('readonly', True)]}),
            'deposit_status' : fields.many2one('item.deposit', 'Deposit Collected'),
            'Applicant_yes': fields.boolean('Co-Applicant'),
            'Applicant_no': fields.boolean('Co-Applicant'),
            'house_id' : fields.many2one('open.house', 'Open-House'),
            'ride_along_id_2' : fields.many2one('res.users', 'Ride-Along'),
            'prod_lot_id' : fields.many2one('stock.production.lot', 'Serial Number'),
            'deposit_amount' : fields.char('Deposit Amount'),
            'same_yes': fields.boolean('Same as Second'),
            'same_no': fields.boolean('Same as Second'),
            'description_2': fields.text('Comments'),
            'lead_type': fields.many2one('crm.lead.type', 'Lead type'),
            'stage_id': fields.selection([('new', 'New'), ('appoint_set', 'Appointment Set'), ('appoint_cancel', 'Appointment Cancelled'), ('demo_in_prog', 'Demo in Progress')], 'Stage', track_visibility='onchange', select=True),
            'source_id': fields.many2one('crm.tracking.source', 'Source', help="This is the source of the link Ex: Search Engine, another domain, or name of email list"),
            
            'lead_id' : fields.many2one('crm.lead', 'Leads'),
            
            'meet_type' : fields.many2one('appointment.type', 'Type'),
            'meeting_location' : fields.many2one('meeting.location', 'Location'),
            'organiser_id' : fields.many2one('res.users', 'Organiser'),
            'meeting_imp' : fields.selection([('normal', 'Normal'), ('low', 'Low'), ('high', 'High')], 'Importance'),
            'trip_to' : fields.char('Trip To'),
            'trip_type' : fields.many2one('trip.type', 'Trip Type'),
            'hotel_name' : fields.char('Hotel Name'),
            
    }
    
    
    def onchange_partner_ids(self, cr, uid, ids, value, context=None):
        """ The basic purpose of this method is to check that destination partners
            effectively have email addresses. Otherwise a warning is thrown.
            :param value: value format: [[6, 0, [3, 4]]]
        """
        res = {'value': {}}

        if not value or not value[0] or not value[0][0] == 6:
            return

        res.update(self.check_partners_email(cr, uid, value[0][2], context=context))
        return res
    
    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {}
    
    _defaults = {
        'name': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'calendar.event'),
        'stage_id' : 'new',
    }
    
    
class res_users(osv.osv):
    _inherit = 'res.users'

    _columns = {
        'dealer_id': fields.many2one('res.dealer', required=True,
            string='Related Dealer', ondelete='restrict',
            help='Dealer-related data of the user'),
    
    }
    
    def create(self, cr, uid, vals, context=None):
        if vals.get('dealer_or_partner') == True:
            dealer_vals = {}
            dealer_vals['name'] = vals.get('name')
            dealer_vals['last_name'] = vals.get('last_name')
            dealer_vals['partner_email'] = vals.get('email')
            dealer_id = self.pool.get('res.dealer').create(cr, uid, dealer_vals)
            vals.update({'dealer_id': dealer_id})
        return super(res_users, self).create(cr, uid, vals, context=context)
    
class sale_order(osv.osv):
    _inherit = "sale.order"
    _columns = {
            'dealer_id' : fields.many2one('res.dealer', 'Dealer'),
            'order_type' : fields.many2one('sale.order.type', 'Type'),
            'personal_no' : fields.char('Personal No'),
    }
    
    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        val = super(sale_order, self).onchange_partner_id(cr, uid, ids, part, context=context)
        if part:
            part = self.pool.get('res.partner').browse(cr, uid, part, context=context)
            val['value']['personal_no'] = part.personal_no
        return val
    
    
class dealer_position(osv.Model):
    _name = 'dealer.position'
    
    _columns = {
            'name' : fields.char('Name'),
    }
class crm_case_section(osv.Model):
    _inherit = 'crm.case.section'

    def _get_opportunities_data(self, cr, uid, ids, field_name, arg, context=None):
        return super(crm_case_section, self)._get_opportunities_data(cr, uid, ids, field_name, arg, context=context)

    _columns = {
        'monthly_planned_revenue': fields.function(_get_opportunities_data,
            type="char", readonly=True, multi='_get_opportunities_data',
            string='Planned Revenue per Month'),
    }

class crm_phonecall(osv.osv):
    """ Model for CRM phonecalls """
    _inherit = "crm.phonecall"
    
    def action_button_convert2opportunity(self, cr, uid, ids, context=None):
        """
        Convert a phonecall into an opp and then redirect to the opp view.

        :param list ids: list of calls ids to convert (typically contains a single id)
        :return dict: containing view information
        """
        return super(crm_phonecall, self).action_button_convert2opportunity(cr, uid, ids, context=context)
    
    def action_make_meeting(self, cr, uid, ids, context=None):
        """
        Open meeting's calendar view to schedule a meeting on current phonecall.
        :return dict: dictionary value for created meeting view
        """
        return super(crm_phonecall, self).action_make_meeting(cr, uid, ids, context=context)
    
    _columns = {
            'dealer_id' : fields.many2one('res.dealer', 'Dealer'),
            'appoint_date' : fields.date('Appointment Date'),
            'appoint_time' : fields.char('Time'),
            'opportunity_id': fields.many2one ('crm.lead', 'Lead/Opportunity'),
    }
class crm_lead2opportunity_partner(osv.osv_memory):
    _inherit = 'crm.lead2opportunity.partner'
    _columns = {
        'name': fields.selection([
                ('convert', 'Convert to demo'),
                ('merge', 'Merge with existing demo')
            ], 'Conversion Action', required=True),
            
    }
    
class account_invoice(osv.osv):
    _inherit = "account.invoice"

    _columns = {
        'dealer_id' : fields.many2one('res.dealer', 'Dealer'),
        'lead_id' : fields.many2one('crm.lead', 'Leads'),
    }

class account_voucher(osv.osv):
    _inherit = 'account.voucher'
    
    _columns = {
        'dealer_id' : fields.many2one('res.dealer', 'Dealer'),
        'lead_id' : fields.many2one('crm.lead', 'Leads'),
    }
    
class item_deliver(osv.Model):
    _name = 'item.deliver'
    
    _columns = {
            'name' : fields.char('Name'),
    }
    
class item_deposit(osv.Model):
    _name = 'item.deposit'
    
    _columns = {
            'name' : fields.char('Name'),
    }

class open_house(osv.Model):
    _name = 'open.house'
    
    _columns = {
            'name' : fields.char('Name'),
    }

class appointment_result(osv.Model):
    _name = 'appointment.result'
    
    _columns = {
            'name' : fields.char('Name'),
    }

class gift_line(osv.Model):
    _name = 'gift.line'
    
    _columns = {
            'partner_id' : fields.many2one('res.partner', 'Partner'),
            'grant_id' : fields.many2one('product.grant', 'HOW GRANTED'),
            'product_id' : fields.many2one('product.product', 'GIFT'),
            'letter_print_date' : fields.date('LETTER PRINTED'),
            'receipt_print_date' : fields.date('RECEIPT PRINTED'),
            'pickup_by' : fields.many2one('res.dealer', 'PICKED UP BY'),
            'receive_date' : fields.date('RECEIVED'),
            'comment' : fields.char('COMMENT'),
            'lead_id' : fields.many2one('crm.lead', 'Leads'),
            'dealer_id' : fields.many2one('res.dealer', 'Dealer'),
    }

class product_grant(osv.Model):
    _name = 'product.grant'
    
    _columns = {
            'name' : fields.char('Name'),
    }

class sale_problem(osv.Model):
    _name = 'sale.problem'
    
    _columns = {
            'name' : fields.char('Name'),
    }

class appt_type(osv.Model):
    _name = 'appt.type'
    
    _columns = {
            'name' : fields.char('Name'),
    }

class payment_type(osv.Model):
    _name = 'payment.type'
    
    _columns = {
            'name' : fields.char('Name'),
    }


class product_warranty(osv.Model):
    _name = 'product.warranty'
    
    _columns = {
            'date' : fields.date('Date'),
            'number' : fields.char('Number'),
            'ref' : fields.char('Ref #'),
            'revision_desc' : fields.char('Revision Description'),
            'total' : fields.integer('Total'),
            'status' : fields.many2one('service.status', 'Status'),
            'partner_warr_id' : fields.many2one('res.partner', 'Partner'),
            'partner_service_id' : fields.many2one('res.partner', 'Partner'),
            
            'lead_warr_id' : fields.many2one('crm.lead', 'Lead'),
            'lead_service_id' : fields.many2one('crm.lead', 'Lead'),
    }
    
    
class service_status(osv.Model):
    _name = 'service.status'
    
    _columns = {
            'name' : fields.char('Name'),
    }

class appointment_type(osv.osv):
    _name = "appointment.type"
    _columns = {
            'name' : fields.char('Name'),
    }

class meeting_location(osv.osv):
    _name = "meeting.location"
    _columns = {
            'name' : fields.char('Name'),
    }

class sale_order_type(osv.osv):
    _name = "sale.order.type"
    _columns = {
            'name' : fields.char('Name'),
    }

class trip_type(osv.osv):
    _name = "trip.type"
    _columns = {
            'name' : fields.char('Name'),
    }

#class campaign_success(osv.osv):
#    _name = "campaign.success"
#    _columns = {
#            'name' : fields.char('Name'),
#    }

class crm_campaign(osv.osv):
    _name = "crm.campaign"
    
    def _compute_days(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        campaign_obj = self.browse(cr, uid, ids)
        curr_date = datetime.toordinal(date.today())
        for campaign in campaign_obj:
            end_date = (datetime.strptime(campaign.end_date , '%Y-%m-%d')).toordinal()
            if end_date >= curr_date:
                day_left = end_date-curr_date
                res[campaign.id] = day_left
            else:
                res[campaign.id] = 0
        return res
        
    _columns = {
    
            'name' : fields.char('Name'),
            'gift_id' : fields.many2one('product.product', 'Gift', domain="[('prod_gift', '=', True)]"),
            'complete_presentation' : fields.char('Completed Presentations'),
            'sale_required' : fields.char('Sales Required'),
            'complete_within_day' : fields.char('Completed Within'),
            'deadline_days' : fields.char('Deadline to Submit Names'),
            'campaign_id' : fields.many2one('crm.campaign', 'Can be earned in conjuction with gift in'),
            'other_campaign_id' : fields.many2one('crm.campaign', 'Other Campaign Completion Required'),
            'end_date' : fields.date('End Date of Campaign'),
            'partner_id' : fields.many2one('res.partner', 'Partner'),
            'lead_id' : fields.many2one('crm.lead', 'Lead'),
            
            'start_date' : fields.date('Start Date'),
            'days_left' : fields.function(_compute_days, string='Days Left', type="integer", store={
                'crm.campaign': (lambda self, cr, uid, ids, c={}: ids, ['end_date'], 10),
            },),
            'required_demos' : fields.char('Required Demos'),
            'realized_demos' : fields.char('Realized Demos'),
            'realized_sales' : fields.char('Realized Sales'),
            'dealer_id' : fields.many2one('res.dealer', 'Dealer'),
            'campaign_success' : fields.selection([('yes', 'Yes'), ('no', 'No')], 'Success'),
    }


class crm_contest(osv.osv):
    _name = "crm.contest"
    
    def _compute_days(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        contest_obj = self.browse(cr, uid, ids)
        curr_date = datetime.toordinal(date.today())
        for contest in contest_obj:
            end_date = (datetime.strptime(contest.end_date , '%Y-%m-%d')).toordinal()
            if end_date >= curr_date:
                day_left = end_date-curr_date
                res[contest.id] = day_left
            else:
                res[contest.id] = 0
        return res
    
    _columns = {
    
            'name' : fields.char('Name'),
            'description' : fields.char('Description'),
            'track_who' : fields.many2one('res.partner', 'Track Who'),
            'start_date' : fields.date('Start Date'),
            'end_date' : fields.date('End Date'),
            'onmy_dash' : fields.boolean('Show On My Dashboard'),
            'ontheir_dash' : fields.many2one('res.partner', 'Show On Their Dashboard'),

            'days_left' : fields.function(_compute_days, string='Days Left', type="integer", store={
                'crm.contest': (lambda self, cr, uid, ids, c={}: ids, ['end_date'], 10),
            },),
            'required_demos' : fields.char('Required Demos'),
            'realized_demos' : fields.char('Realized Demos'),
            'required_sales' : fields.char('Required Sales'),
            'realized_sales' : fields.char('Realized Sales'),
            'dealer_id' : fields.many2one('res.dealer', 'Dealer'),
            'campaign_success' : fields.selection([('yes', 'Yes'), ('no', 'No')], 'Success'),
            'gift_id' : fields.many2one('product.product', 'Gift', domain="[('prod_gift', '=', True)]"),
            
    }

class item_sold(osv.osv):
    _name = 'item.sold'
    
    _columns = {
            'partner_id' : fields.many2one('res.partner', 'Partner'),
            'product_id' : fields.many2one('product.product', 'ITEM'),
            'serial_no' : fields.many2one('stock.production.lot', 'SERIAL NUMBER'),
            'consign_id' : fields.many2one('stock.location', 'CONSIGNED TO'),
            'consign_date' : fields.datetime('CONSIGN DATE'),
            'contract_id' : fields.many2one('account.analytic.account', 'CONTRACT NO'),
    }

class product_consignment(osv.osv):
    _name = 'product.consignment'
    _columns = {
            'product_id' : fields.many2one('product.product', 'ITEM'),
            'serial_no' : fields.many2one('stock.production.lot', 'SERIAL #'),
            'consign_date' : fields.date('DATE CONSIGNED'),
            'return_date' : fields.date('DATE RETURNED'),
            'partner_id' : fields.many2one('res.partner', 'CUSTOMER'),
            'dealer_id' : fields.many2one('res.dealer', 'Dealer'),
    
    }
    
class crm_lead_type(osv.osv):
    _name = 'crm.lead.type'
    _columns = {
            'name' : fields.char('Lead Type', required=True),
    }
    
class crm_lead2appointment(osv.osv_memory):
    _name = 'crm.lead2appointment'

    _columns = {
            'start_datetime' : fields.datetime('Starting at', required=True),
            'stop_datetime' : fields.datetime('Ending at', required=True),
    }
    
    def action_apply(self, cr, uid, ids, context=None):
        vals = {}
        Lead_obj = self.pool.get('crm.lead')
        crm_lead_obj = Lead_obj.browse(cr, uid, context.get('active_id'))
        wizard = self.browse(cr, uid, ids)
        vals = {'first_name' : crm_lead_obj.name,
                'last_name' : crm_lead_obj.last_name,
                'start_datetime' : wizard.start_datetime,
                'stop_datetime' : wizard.stop_datetime,
                'stage_id' :'new',
                'image' : crm_lead_obj.image,}
        self.pool.get('calendar.event').create(cr, uid, vals)
        stage_id = self.pool.get('crm.case.stage').search(cr, uid, [('name', '=', 'Appointment Set'), ('type', 'in', ['lead', 'both'])])[0]
        Lead_obj.write(cr, uid, context.get('active_id'), {'stage_id': stage_id})
        return {'type': 'ir.actions.act_window_close'}
