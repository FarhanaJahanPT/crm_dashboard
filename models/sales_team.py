from odoo import models, fields, api
from datetime import date

from odoo.tools import date_utils


class SalesTeam(models.Model):

    _inherit = "crm.team"


    state_id = fields.Many2one('crm.stage',string="State")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        super(SaleOrder, self).action_confirm()
        self.team_id.state_id = self.opportunity_id.stage_id

class CRMLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_dashboard_data(self):
        crm_lead = self.env['crm.lead']

        total_leads = crm_lead.search_count([('type', '=', 'lead'),('user_id','=',self.env.user.id)])
        total_opportunities = crm_lead.search_count([('type', '=', 'opportunity'),('user_id','=',self.env.user.id)])
        total_exp_revenue = sum(crm_lead.search([('type', '=', 'opportunity'),('user_id','=',self.env.user.id)]).mapped('expected_revenue'))
        total_revenue = sum(crm_lead.search([('type', '=', 'opportunity'),('user_id','=',self.env.user.id),('stage_id','=', 'Won')]).mapped('expected_revenue'))
        total_win = sum(crm_lead.search([('stage_id','=', 'Won')]).mapped('expected_revenue'))
        total_lost = sum(crm_lead.search([('active','=',False)]).mapped('expected_revenue'))
        win_ratio = total_win/total_lost
        ratio = round(win_ratio,2)



        return {
            'total_leads':total_leads,
            'total_opportunities':total_opportunities,
            'total_exp_revenue':total_exp_revenue,
            'total_revenue':total_revenue,
            'ratio':ratio,
        }
    @api.model
    def get_the_lead_year(self):
        crm_lead = self.env['crm.lead']

        total_lead_stage = crm_lead.search([('type', '=', 'lead')]).filtered(lambda l: l.create_date.year==date.today().year).mapped('stage_id.name')
        total_lead_stage_new = crm_lead.search([('type', '=', 'lead'),('stage_id','=','New')]).filtered(lambda l: l.create_date.year==date.today().year)
        total_lead_stage_qualified = crm_lead.search([('type', '=', 'lead'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date.year==date.today().year)
        total_lead_stage_prop = crm_lead.search([('type', '=', 'lead'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date.year==date.today().year)
        # total_lead_stage = crm_lead.search([('type', '=', 'lead'),('user_id','=',self.env.user.id)]).mapped('stage_id.name')
        print(total_lead_stage_new ,'jhgfds')

        return {
            'total_lead_stage':total_lead_stage,
            'total_lead_stage_new':len(total_lead_stage_new),
            'total_lead_stage_qualified':len(total_lead_stage_qualified),
            'total_lead_stage_prop':len(total_lead_stage_prop),
        }

    @api.model
    def get_the_lead_week(self):
        crm_lead = self.env['crm.lead']

        total_lead_stage = crm_lead.search([('type', '=', 'lead')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('stage_id.name')
        total_lead_stage_new = crm_lead.search([('type', '=', 'lead'),('stage_id','=','New')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1])
        total_lead_stage_qualified = crm_lead.search([('type', '=', 'lead'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1])
        total_lead_stage_prop = crm_lead.search([('type', '=', 'lead'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1])
        # total_lead_stage = crm_lead.search([('type', '=', 'lead'),('user_id','=',self.env.user.id)]).mapped('stage_id.name')
        print(total_lead_stage_new ,'jhgfds')

        return {
            'total_lead_stage':total_lead_stage,
            'total_lead_stage_new':len(total_lead_stage_new),
            'total_lead_stage_qualified':len(total_lead_stage_qualified),
            'total_lead_stage_prop':len(total_lead_stage_prop),
        }
    @api.model
    def get_the_lead_month(self):
        crm_lead = self.env['crm.lead']

        total_lead_stage = crm_lead.search([('type', '=', 'lead')]).filtered(lambda l: l.create_date.month==date.today().month).mapped('stage_id.name')
        total_lead_stage_new = crm_lead.search([('type', '=', 'lead'),('stage_id','=','New')]).filtered(lambda l: l.create_date.month==date.today().month)
        total_lead_stage_qualified = crm_lead.search([('type', '=', 'lead'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date.month==date.today().month)
        total_lead_stage_prop = crm_lead.search([('type', '=', 'lead'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date.month==date.today().month)
        # total_lead_stage = crm_lead.search([('type', '=', 'lead'),('user_id','=',self.env.user.id)]).mapped('stage_id.name')
        print(total_lead_stage_new ,'jhgfds')

        return {
            'total_lead_stage':total_lead_stage,
            'total_lead_stage_new':len(total_lead_stage_new),
            'total_lead_stage_qualified':len(total_lead_stage_qualified),
            'total_lead_stage_prop':len(total_lead_stage_prop),
        }
    @api.model
    def get_the_lead_quarter(self):
        start_date,end_date = date_utils.get_quarter(fields.datetime.today())
        crm_lead = self.env['crm.lead']

        total_lead_stage = crm_lead.search([('type', '=', 'lead')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date).mapped('stage_id.name')
        total_lead_stage_new = crm_lead.search([('type', '=', 'lead'),('stage_id','=','New')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date)
        total_lead_stage_qualified = crm_lead.search([('type', '=', 'lead'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date)
        total_lead_stage_prop = crm_lead.search([('type', '=', 'lead'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date)
        # total_lead_stage = crm_lead.search([('type', '=', 'lead'),('user_id','=',self.env.user.id)]).mapped('stage_id.name')
        print(total_lead_stage_new ,'jhgfds')

        return {
            'total_lead_stage':total_lead_stage,
            'total_lead_stage_new':len(total_lead_stage_new),
            'total_lead_stage_qualified':len(total_lead_stage_qualified),
            'total_lead_stage_prop':len(total_lead_stage_prop),
        }




    @api.model
    def get_the_opportunity_year(self):
        crm_lead = self.env['crm.lead']

        total_opportunity_stage = crm_lead.search([('type', '=', 'opportunity')]).filtered(lambda l: l.create_date.year==date.today().year).mapped('stage_id.name')
        total_opportunity_stage_new = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New')]).filtered(lambda l: l.create_date.year==date.today().year)
        total_opportunity_stage_qualified = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date.year==date.today().year)
        total_opportunity_stage_prop = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date.year==date.today().year)
        total_opportunity_stage_won = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Won')]).filtered(lambda l: l.create_date.year==date.today().year)
        # print(total_lead_stage_new ,'jhgfds')

        return {
            'total_opportunity_stage':total_opportunity_stage,
            'total_opportunity_stage_new':len(total_opportunity_stage_new),
            'total_opportunity_stage_qualified':len(total_opportunity_stage_qualified),
            'total_opportunity_stage_prop':len(total_opportunity_stage_prop),
            'total_opportunity_stage_won':len(total_opportunity_stage_won),
        }
    @api.model
    def get_the_opportunity_month(self):
        crm_lead = self.env['crm.lead']

        total_opportunity_stage = crm_lead.search([('type', '=', 'opportunity')]).filtered(lambda l: l.create_date.month==date.today().month).mapped('stage_id.name')
        total_opportunity_stage_new = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New')]).filtered(lambda l: l.create_date.month==date.today().month)
        total_opportunity_stage_qualified = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date.month==date.today().month)
        total_opportunity_stage_prop = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date.month==date.today().month)
        total_opportunity_stage_won = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Won')]).filtered(lambda l: l.create_date.month==date.today().month)
        # print(total_lead_stage_new ,'jhgfds')

        return {
            'total_opportunity_stage':total_opportunity_stage,
            'total_opportunity_stage_new':len(total_opportunity_stage_new),
            'total_opportunity_stage_qualified':len(total_opportunity_stage_qualified),
            'total_opportunity_stage_prop':len(total_opportunity_stage_prop),
            'total_opportunity_stage_won':len(total_opportunity_stage_won),
        }
    @api.model
    def get_the_opportunity_week(self):
        crm_lead = self.env['crm.lead']

        total_opportunity_stage = crm_lead.search([('type', '=', 'opportunity')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('stage_id.name')
        total_opportunity_stage_new = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1])
        total_opportunity_stage_qualified = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1])
        total_opportunity_stage_prop = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1])
        total_opportunity_stage_won = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Won')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1])
        # print(total_lead_stage_new ,'jhgfds')

        return {
            'total_opportunity_stage':total_opportunity_stage,
            'total_opportunity_stage_new':len(total_opportunity_stage_new),
            'total_opportunity_stage_qualified':len(total_opportunity_stage_qualified),
            'total_opportunity_stage_prop':len(total_opportunity_stage_prop),
            'total_opportunity_stage_won':len(total_opportunity_stage_won),
        }
    @api.model
    def get_the_opportunity_quarter(self):
        start_date,end_date = date_utils.get_quarter(fields.datetime.today())
        crm_lead = self.env['crm.lead']

        total_opportunity_stage = crm_lead.search([('type', '=', 'opportunity')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date).mapped('stage_id.name')
        total_opportunity_stage_new = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date)
        total_opportunity_stage_qualified = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date)
        total_opportunity_stage_prop = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date)
        total_opportunity_stage_won = crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Won')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date)
        # print(total_lead_stage_new ,'jhgfds')

        return {
            'total_opportunity_stage':total_opportunity_stage,
            'total_opportunity_stage_new':len(total_opportunity_stage_new),
            'total_opportunity_stage_qualified':len(total_opportunity_stage_qualified),
            'total_opportunity_stage_prop':len(total_opportunity_stage_prop),
            'total_opportunity_stage_won':len(total_opportunity_stage_won),
        }



    @api.model
    def get_total_exp_revenue_year(self):
        crm_lead = self.env['crm.lead']

        total_opportunity_stage = crm_lead.search([('type', '=', 'opportunity')]).filtered(lambda l: l.create_date.year==date.today().year).mapped('stage_id.name')

        total_opportunity_exp_stage_new = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New')]).filtered(lambda l: l.create_date.year==date.today().year).mapped('expected_revenue'))
        total_opportunity_exp_stage_qualified = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date.year==date.today().year).mapped('expected_revenue'))
        print(total_opportunity_exp_stage_qualified)
        total_opportunity_exp_stage_prop = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date.year==date.today().year).mapped('expected_revenue'))
        total_opportunity_exp_stage_won = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Won')]).filtered(lambda l: l.create_date.year==date.today().year).mapped('expected_revenue'))

        return {
            'total_opportunity_stage':total_opportunity_stage,
            'total_opportunity_exp_stage_new':total_opportunity_exp_stage_new,
            'total_opportunity_exp_stage_qualified':total_opportunity_exp_stage_qualified,
            'total_opportunity_exp_stage_prop':total_opportunity_exp_stage_prop,
            'total_opportunity_exp_stage_won':total_opportunity_exp_stage_won,
        }

    @api.model
    def get_total_exp_revenue_month(self):
        crm_lead = self.env['crm.lead']

        total_opportunity_stage = crm_lead.search([('type', '=', 'opportunity')]).filtered(lambda l: l.create_date.month==date.today().month).mapped('stage_id.name')

        total_opportunity_exp_stage_new = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New')]).filtered(lambda l: l.create_date.month==date.today().month).mapped('expected_revenue'))
        total_opportunity_exp_stage_qualified = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date.month==date.today().month).mapped('expected_revenue'))
        print(total_opportunity_exp_stage_qualified)
        total_opportunity_exp_stage_prop = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date.month==date.today().month).mapped('expected_revenue'))
        total_opportunity_exp_stage_won = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Won')]).filtered(lambda l: l.create_date.month==date.today().month).mapped('expected_revenue'))

        return {
            'total_opportunity_stage':total_opportunity_stage,
            'total_opportunity_exp_stage_new':total_opportunity_exp_stage_new,
            'total_opportunity_exp_stage_qualified':total_opportunity_exp_stage_qualified,
            'total_opportunity_exp_stage_prop':total_opportunity_exp_stage_prop,
            'total_opportunity_exp_stage_won':total_opportunity_exp_stage_won,
        }

    @api.model
    def get_total_exp_revenue_week(self):
        crm_lead = self.env['crm.lead']

        total_opportunity_stage = crm_lead.search([('type', '=', 'opportunity')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('stage_id.name')

        total_opportunity_exp_stage_new = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('expected_revenue'))
        total_opportunity_exp_stage_qualified = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('expected_revenue'))
        print(total_opportunity_exp_stage_qualified)
        total_opportunity_exp_stage_prop = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('expected_revenue'))
        total_opportunity_exp_stage_won = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Won')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('expected_revenue'))

        return {
            'total_opportunity_stage':total_opportunity_stage,
            'total_opportunity_exp_stage_new':total_opportunity_exp_stage_new,
            'total_opportunity_exp_stage_qualified':total_opportunity_exp_stage_qualified,
            'total_opportunity_exp_stage_prop':total_opportunity_exp_stage_prop,
            'total_opportunity_exp_stage_won':total_opportunity_exp_stage_won,
        }

    @api.model
    def get_total_exp_revenue_quarter(self):
        start_date,end_date = date_utils.get_quarter(fields.datetime.today())
        crm_lead = self.env['crm.lead']

        total_opportunity_stage = crm_lead.search([('type', '=', 'opportunity')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date).mapped('stage_id.name')

        total_opportunity_exp_stage_new = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date).mapped('expected_revenue'))
        total_opportunity_exp_stage_qualified = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date).mapped('expected_revenue'))
        print(total_opportunity_exp_stage_qualified)
        total_opportunity_exp_stage_prop = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date).mapped('expected_revenue'))
        total_opportunity_exp_stage_won = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','Won')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date).mapped('expected_revenue'))

        return {
            'total_opportunity_stage':total_opportunity_stage,
            'total_opportunity_exp_stage_new':total_opportunity_exp_stage_new,
            'total_opportunity_exp_stage_qualified':total_opportunity_exp_stage_qualified,
            'total_opportunity_exp_stage_prop':total_opportunity_exp_stage_prop,
            'total_opportunity_exp_stage_won':total_opportunity_exp_stage_won,
        }


    @api.model
    def get_total_revenue_year(self):
        crm_lead = self.env['crm.lead']

        total_opportunity_stage_won = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=', 'Won')]).filtered(lambda l: l.create_date.year==date.today().year).mapped('expected_revenue'))

        total_opportunity_exp_stage_others_a = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New')]).filtered(lambda l: l.create_date.year==date.today().year).mapped('expected_revenue'))
        total_opportunity_exp_stage_others_b = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date.year==date.today().year).mapped('expected_revenue'))
        total_opportunity_exp_stage_others_c = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New'),('stage_id','=','Qualified'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date.year==date.today().year).mapped('expected_revenue'))
        total_opportunity_exp_stage_others = (total_opportunity_exp_stage_others_a + total_opportunity_exp_stage_others_b + total_opportunity_exp_stage_others_c)
        print(total_opportunity_stage_won)
        print(total_opportunity_exp_stage_others,'kk')

        return {
            'total_opportunity_stage_won':total_opportunity_stage_won,
            'total_opportunity_exp_stage_others':total_opportunity_exp_stage_others,
        }


    @api.model
    def get_total_revenue_month(self):
        crm_lead = self.env['crm.lead']

        total_opportunity_stage_won = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=', 'Won')]).filtered(lambda l: l.create_date.month==date.today().month).mapped('expected_revenue'))

        total_opportunity_exp_stage_others_a = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New')]).filtered(lambda l: l.create_date.month==date.today().month).mapped('expected_revenue'))
        total_opportunity_exp_stage_others_b = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date.month==date.today().month).mapped('expected_revenue'))
        total_opportunity_exp_stage_others_c = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New'),('stage_id','=','Qualified'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date.month==date.today().month).mapped('expected_revenue'))
        total_opportunity_exp_stage_others = (total_opportunity_exp_stage_others_a + total_opportunity_exp_stage_others_b + total_opportunity_exp_stage_others_c)
        print(total_opportunity_stage_won)
        print(total_opportunity_exp_stage_others,'kk')

        return {
            'total_opportunity_stage_won':total_opportunity_stage_won,
            'total_opportunity_exp_stage_others':total_opportunity_exp_stage_others,
        }


    @api.model
    def get_total_revenue_week(self):
        crm_lead = self.env['crm.lead']

        total_opportunity_stage_won = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=', 'Won')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('expected_revenue'))

        total_opportunity_exp_stage_others_a = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('expected_revenue'))
        total_opportunity_exp_stage_others_b = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('expected_revenue'))
        total_opportunity_exp_stage_others_c = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New'),('stage_id','=','Qualified'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('expected_revenue'))
        total_opportunity_exp_stage_others = (total_opportunity_exp_stage_others_a + total_opportunity_exp_stage_others_b + total_opportunity_exp_stage_others_c)
        print(total_opportunity_stage_won)
        print(total_opportunity_exp_stage_others,'kk')

        return {
            'total_opportunity_stage_won':total_opportunity_stage_won,
            'total_opportunity_exp_stage_others':total_opportunity_exp_stage_others,
        }


    @api.model
    def get_total_revenue_quarter(self):
        crm_lead = self.env['crm.lead']
        start_date,end_date = date_utils.get_quarter(fields.datetime.today())

        total_opportunity_stage_won = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=', 'Won')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date).mapped('expected_revenue'))

        total_opportunity_exp_stage_others_a = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date).mapped('expected_revenue'))
        total_opportunity_exp_stage_others_b = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New'),('stage_id','=','Qualified')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date).mapped('expected_revenue'))
        total_opportunity_exp_stage_others_c = sum(crm_lead.search([('type', '=', 'opportunity'),('stage_id','=','New'),('stage_id','=','Qualified'),('stage_id','=','Proposition')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date).mapped('expected_revenue'))
        total_opportunity_exp_stage_others = (total_opportunity_exp_stage_others_a + total_opportunity_exp_stage_others_b + total_opportunity_exp_stage_others_c)
        print(total_opportunity_stage_won)
        print(total_opportunity_exp_stage_others,'kk')

        return {
            'total_opportunity_stage_won':total_opportunity_stage_won,
            'total_opportunity_exp_stage_others':total_opportunity_exp_stage_others,
        }

    @api.model
    def get_win_ratio_year(self):
        crm_lead = self.env['crm.lead']

        total_win_ratio = sum(crm_lead.search([('stage_id', '=', 'Won')]).filtered(lambda l: l.create_date.year==date.today().year).mapped('expected_revenue'))
        total_lost_ratio = sum(crm_lead.search([('active', '=', False)]).filtered(lambda l: l.create_date.year==date.today().year).mapped('expected_revenue'))
        total_lost_win_ratio = total_win_ratio+total_lost_ratio
        if total_lost_win_ratio==0:
            ratio_of_win = 1
            ratio_of_lost = 1
        else:
            ratio_of_win =(total_win_ratio/total_lost_win_ratio)*100
            ratio_of_lost =(total_lost_ratio/total_lost_win_ratio)*100

        return {
            'ratio_of_win':ratio_of_win,
            'ratio_of_lost':ratio_of_lost,
        }


    @api.model
    def get_win_ratio_month(self):
        crm_lead = self.env['crm.lead']

        total_win_ratio = sum(crm_lead.search([('stage_id', '=', 'Won')]).filtered(lambda l: l.create_date.month==date.today().month).mapped('expected_revenue'))
        total_lost_ratio = sum(crm_lead.search([('active', '=', False)]).filtered(lambda l: l.create_date.month==date.today().month).mapped('expected_revenue'))
        total_lost_win_ratio = total_win_ratio+total_lost_ratio
        if total_lost_win_ratio==0:
            ratio_of_win = 1
            ratio_of_lost = 1
        else:
            ratio_of_win =(total_win_ratio/total_lost_win_ratio)*100
            ratio_of_lost =(total_lost_ratio/total_lost_win_ratio)*100

        return {
            'ratio_of_win':ratio_of_win,
            'ratio_of_lost':ratio_of_lost,
        }


    @api.model
    def get_win_ratio_week(self):
        crm_lead = self.env['crm.lead']

        total_win_ratio = sum(crm_lead.search([('stage_id', '=', 'Won')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('expected_revenue'))
        total_lost_ratio = sum(crm_lead.search([('active', '=', False)]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('expected_revenue'))
        total_lost_win_ratio = total_win_ratio+total_lost_ratio
        if total_lost_win_ratio==0:
            ratio_of_win = 1
            ratio_of_lost = 1
        else:
            ratio_of_win =(total_win_ratio/total_lost_win_ratio)*100
            ratio_of_lost =(total_lost_ratio/total_lost_win_ratio)*100

        return {
            'ratio_of_win':ratio_of_win,
            'ratio_of_lost':ratio_of_lost,
        }


    @api.model
    def get_win_ratio_quarter(self):
        crm_lead = self.env['crm.lead']
        start_date,end_date = date_utils.get_quarter(fields.datetime.today())

        total_win_ratio = sum(crm_lead.search([('stage_id', '=', 'Won')]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date).mapped('expected_revenue'))
        total_lost_ratio = sum(crm_lead.search([('active', '=', False)]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date).mapped('expected_revenue'))
        total_lost_win_ratio = total_win_ratio+total_lost_ratio
        if total_lost_win_ratio==0:
            ratio_of_win = 1
            ratio_of_lost = 1
        else:
            ratio_of_win =(total_win_ratio/total_lost_win_ratio)*100
            ratio_of_lost =(total_lost_ratio/total_lost_win_ratio)*100

        return {
            'ratio_of_win':ratio_of_win,
            'ratio_of_lost':ratio_of_lost,
        }

    @api.model
    def crm_year(self):
        crm_lead = self.env['crm.lead']
        total_leads_year = crm_lead.search([('type', '=', 'lead'),('user_id','=',self.env.user.id)]).filtered(lambda l: l.create_date.year==date.today().year)
        total_opportunities_year = crm_lead.search([('type', '=', 'opportunity'),('user_id','=',self.env.user.id)]).filtered(lambda l: l.create_date.year==date.today().year)
        total_exp_revenue_year = crm_lead.search([('type', '=', 'opportunity'),('user_id','=',self.env.user.id)]).filtered(lambda l: l.create_date.year==date.today().year).mapped('expected_revenue')
        total_revenue_year = crm_lead.search([('type', '=', 'opportunity'),('user_id','=',self.env.user.id),('stage_id','=', 'Won')]).filtered(lambda l: l.create_date.year==date.today().year).mapped('expected_revenue')
        total_win_year = sum(crm_lead.search([('stage_id', '=', 'Won')]).filtered(lambda l: l.create_date.year==date.today().year).mapped('expected_revenue'))
        total_lost_year = sum(crm_lead.search([('active', '=', False)]).filtered(lambda l: l.create_date.year==date.today().year).mapped('expected_revenue'))
        win_ratio_year = total_win_year / total_lost_year
        ratio_year = round(win_ratio_year, 2)
        return {
            'total_leads_year':len(total_leads_year),
            'total_opportunities_year':len(total_opportunities_year),
            'total_exp_revenue_year':sum(total_exp_revenue_year),
            'total_revenue_year':sum(total_revenue_year),
            'ratio_year':ratio_year,
        }

    @api.model
    def crm_month(self):
        crm_lead = self.env['crm.lead']
        total_leads_month = crm_lead.search([('type', '=', 'lead'),('user_id','=',self.env.user.id)]).filtered(lambda l: l.create_date.month==date.today().month)
        total_opportunities_month = crm_lead.search([('type', '=', 'opportunity'),('user_id','=',self.env.user.id)]).filtered(lambda l: l.create_date.month==date.today().month)
        total_exp_revenue_month = crm_lead.search([('type', '=', 'opportunity'),('user_id','=',self.env.user.id)]).filtered(lambda l: l.create_date.month==date.today().month).mapped('expected_revenue')
        total_revenue_month = crm_lead.search([('type', '=', 'opportunity'),('user_id','=',self.env.user.id),('stage_id','=', 'Won')]).filtered(lambda l: l.create_date.month==date.today().month).mapped('expected_revenue')
        total_win_month = sum(crm_lead.search([('stage_id', '=', 'Won')]).filtered(lambda l: l.create_date.month==date.today().month).mapped('expected_revenue'))
        total_lost_month = sum(crm_lead.search([('active', '=', False)]).filtered(lambda l: l.create_date.month==date.today().month).mapped('expected_revenue'))
        win_ratio_month = total_win_month / total_lost_month
        ratio_month = round(win_ratio_month, 2)
        return {
            'total_leads_month':len(total_leads_month),
            'total_opportunities_month':len(total_opportunities_month),
            'total_exp_revenue_month':sum(total_exp_revenue_month),
            'total_revenue_month':sum(total_revenue_month),
            'ratio_month':ratio_month,
        }
    @api.model
    def crm_week(self):
        crm_lead = self.env['crm.lead']
        total_leads_week = crm_lead.search([('type', '=', 'lead'),('user_id','=',self.env.user.id)]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1])
        total_opportunities_week = crm_lead.search([('type', '=', 'opportunity'),('user_id','=',self.env.user.id)]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1])
        total_exp_revenue_week = crm_lead.search([('type', '=', 'opportunity'),('user_id','=',self.env.user.id)]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('expected_revenue')
        total_revenue_week = crm_lead.search([('type', '=', 'opportunity'),('user_id','=',self.env.user.id),('stage_id','=', 'Won')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('expected_revenue')
        total_win_week = sum(crm_lead.search([('stage_id', '=', 'Won')]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('expected_revenue'))
        total_lost_week = sum(crm_lead.search([('active', '=', False)]).filtered(lambda l: l.create_date.isocalendar()[1]==date.today().isocalendar()[1]).mapped('expected_revenue'))
        print(total_lost_week,'lkjhgfd')
        if total_lost_week == 0:
            ratio_week = 1
        else:
            win_ratio_week = total_win_week / total_lost_week
            ratio_week = round(win_ratio_week, 2)
        return {
            'total_leads_week':len(total_leads_week),
            'total_opportunities_week':len(total_opportunities_week),
            'total_exp_revenue_week':sum(total_exp_revenue_week),
            'total_revenue_week':sum(total_revenue_week),
            'ratio_week':ratio_week,
        }
    @api.model
    def crm_quarter(self):
        start_date,end_date = date_utils.get_quarter(fields.datetime.today())
        print(start_date)
        print(end_date)
        crm_lead = self.env['crm.lead']
        total_leads_quarter = crm_lead.search([('type', '=', 'lead'),('user_id','=',self.env.user.id)]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date)
        total_opportunities_quarter = crm_lead.search([('type', '=', 'opportunity'),('user_id','=',self.env.user.id)]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date)
        total_exp_revenue_quarter = crm_lead.search([('type', '=', 'opportunity'),('user_id','=',self.env.user.id)]).filtered(lambda l: l.create_date>=start_date and l.create_date <= end_date).mapped('expected_revenue')
        total_revenue_quarter = crm_lead.search([('type', '=', 'opportunity'),('user_id','=',self.env.user.id),('stage_id','=', 'Won')]).filtered(lambda l: l.create_date >= start_date and l.create_date <= end_date).mapped('expected_revenue')
        total_win_quarter = sum(crm_lead.search([('stage_id', '=', 'Won')]).filtered(lambda l: l.create_date >= start_date and l.create_date <= end_date).mapped('expected_revenue'))
        total_lost_quarter = sum(crm_lead.search([('active', '=', False)]).filtered(lambda l: l.create_date >= start_date and l.create_date <= end_date).mapped('expected_revenue'))
        win_ratio_quarter = total_win_quarter / total_lost_quarter
        ratio_quarter = round(win_ratio_quarter, 2)

        return {
            'total_leads_quarter':len(total_leads_quarter),
            'total_opportunities_quarter':len(total_opportunities_quarter),
            'total_exp_revenue_quarter':sum(total_exp_revenue_quarter),
            'total_revenue_quarter':sum(total_revenue_quarter),
            'ratio_quarter':ratio_quarter,
        }


