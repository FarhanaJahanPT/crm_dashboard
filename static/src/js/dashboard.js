odoo.define('crm_dashboard.dashboard_action', function (require){
"use strict";
var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var QWeb = core.qweb;
var rpc = require('web.rpc');
var session = require('web.session');
var ajax = require('web.ajax');
var CustomDashBoard = AbstractAction.extend({
   template: 'CustomDashBoard',
    events: {
            'click #my_lead_dashboard': 'my_lead',
            'click #my_opportunity_dashboard': 'opportunity',
            'click #my_exp_revenue_dashboard': 'exp_revenue',
            'click #my_revenue_dashboard': 'revenue',
            'change #income_expense_values': function(e) {
                e.stopPropagation();
                var $target = $(e.target);
                var value = $target.val();
                if (value=="this_year"){
                    this.onclick_this_year($target.val());
                }else if (value=="this_quarter"){
                    this.onclick_this_quarter($target.val());
                }else if (value=="this_month"){
                    this.onclick_this_month($target.val());
                }else if (value=="this_week"){
                    this.onclick_this_week($target.val());
                }
            },
            },
   init: function(parent, context) {
       this._super(parent, context);
       this.dashboards_templates = ['DashboardProject','Managercrm'];
       this.today_sale = [];
   },
   willStart: function() {
       var self = this;
       return $.when(ajax.rpc(this), this._super()).then(function() {
           return self.fetch_data();
       });
       },
   start: function() {
           var self = this;
           this.set("title", 'Dashboard');
           return this._super().then(function() {
               self.render_dashboards();
               self.render_graphs();
               self.$("#activity_week").hide()
                         self.$("#activity_month").show()
                         self.$("#activity_year").hide()
                         self.$("#activity_week").hide()
                         self.$("#activity_month").hide()

                         self.$("#opportunity_month").show()
                         self.$("#opportunity_year").hide()
                         self.$("#opportunity_week").hide()
                         self.$("#opportunity_quarter").hide()

                         self.$("#total_revenue_month").show()
                         self.$("#total_revenue_year").hide()
                         self.$("#total_revenue_week").hide()
                         self.$("#total_revenue_quarter").hide()

                         self.$("#total_comp_revenue_month").show()
                         self.$("#total_comp_revenue_year").hide()
                         self.$("#total_comp_revenue_week").hide()
                         self.$("#total_comp_revenue_quarter").hide()

                         self.$("#win_ratio_expense_month").show()
                         self.$("#win_ratio_expense_year").hide()
                         self.$("#win_ratio_expense_week").hide()
                         self.$("#win_ratio_expense_quarter").hide()

           });
       },
            render_graphs: function(){
            var self = this;
            self.render_the_lead_graph();
            },
       render_dashboards: function(){
       var self = this;
       _.each(this.dashboards_templates, function(template) {
               self.$('.o_pj_dashboard').append(QWeb.render(template, {widget: self}));
           });
   },
   my_lead: function() {
   console.log(session.uid,'session.uid')


            this.do_action({
                name: ("My Leads"),
                type: 'ir.actions.act_window',
                res_model: 'crm.lead',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['user_id', '=', session.uid],['type', '=', 'lead']],
                target: 'current',
            })
        },
   opportunity: function() {


           this.do_action({
                name: ("Opportunity"),
                type: 'ir.actions.act_window',
                res_model: 'crm.lead',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['user_id', '=', session.uid], ['type','=', 'opportunity']],
                target: 'current',
            })
        },
   exp_revenue: function() {

           this.do_action({
                name: ("Expected Revenue"),
                type: 'ir.actions.act_window',
                res_model: 'crm.lead',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['user_id','=', session.uid], ['type','=', 'opportunity'], ['active','=', true]],
                target: 'current',
            })
        },
   revenue: function() {

           this.do_action({
                name: ("Revenue"),
                type: 'ir.actions.act_window',
                res_model: 'crm.lead',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['user_id','=', session.uid], ['type','=', 'opportunity'], ['stage_id','=', 4]],
                target: 'current',
            })
        },



fetch_data: function() {
        console.log('kjhgfd')
       var self = this;
       var def1 =  this._rpc({
               model: 'crm.lead',
               method: 'get_dashboard_data',
   }).then(function(result)
    {
      $("#lead_dashboard").append('<span>'+result.total_leads+'</span>')
      $("#opportunity_dashboard").append('<span>'+result.total_opportunities+'</span>')
      $("#expected_revenue_dashboard").append('<span>'+result.total_exp_revenue+'</span>')
      $("#total_revenue_dashboard").append('<span>'+result.total_revenue+'</span>')
      $("#win_ratio_dashboard").append('<span>'+result.ratio+'</span>')

   });

   },

render_the_lead_graph:function(){
    console.log('p')
            var self = this
            var ctx = self.$(".total_lead_year");
            rpc.query({
                model: "crm.lead",
                method: "get_the_lead_year",
            }).then(function (result) {
                self.total_lead_stage = result['total_lead_stage'],
                self.total_lead_stage_new = result['total_lead_stage_new'],
                self.total_lead_stage_qualified = result['total_lead_stage_qualified'],
                self.total_lead_stage_prop = result['total_lead_stage_prop'],
                console.log(result,'hgfds')
       const ctx = $('#activity_year')

          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: result['total_lead_stage'],
              datasets: [{
                label: 'Stage',
                data: [result['total_lead_stage_new'],result['total_lead_stage_qualified'],result['total_lead_stage_prop']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });

            var self = this
            var ctx = self.$(".total_lead_month");
            rpc.query({
                model: "crm.lead",
                method: "get_the_lead_month",
            }).then(function (result) {
                self.total_lead_stage = result['total_lead_stage'],
                self.total_lead_stage_new = result['total_lead_stage_new'],
                self.total_lead_stage_qualified = result['total_lead_stage_qualified'],
                self.total_lead_stage_prop = result['total_lead_stage_prop'],
                console.log(result,'hgfds')
       const ctx = $('#activity_month')

          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: result['total_lead_stage'],
              datasets: [{
                label: 'Stage',
                data: [result['total_lead_stage_new'],result['total_lead_stage_qualified'],result['total_lead_stage_prop']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });

             var self = this
            var ctx = self.$(".total_lead_quarter");
            rpc.query({
                model: "crm.lead",
                method: "get_the_lead_quarter",
            }).then(function (result) {
                self.total_lead_stage = result['total_lead_stage'],
                self.total_lead_stage_new = result['total_lead_stage_new'],
                self.total_lead_stage_qualified = result['total_lead_stage_qualified'],
                self.total_lead_stage_prop = result['total_lead_stage_prop'],
                console.log(result,'hgfds')
       const ctx = $('#activity_quarter')

          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: result['total_lead_stage'],
              datasets: [{
                label: 'Stage',
                data: [result['total_lead_stage_new'],result['total_lead_stage_qualified'],result['total_lead_stage_prop']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });


            var ctx = self.$(".total_lead_week");
            rpc.query({
                model: "crm.lead",
                method: "get_the_lead_week",
            }).then(function (result) {
                self.total_lead_stage = result['total_lead_stage'],
                self.total_lead_stage_new = result['total_lead_stage_new'],
                self.total_lead_stage_qualified = result['total_lead_stage_qualified'],
                self.total_lead_stage_prop = result['total_lead_stage_prop'],
                console.log(result,'hgfds')
       const ctx = $('#activity_week')

          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: result['total_lead_stage'],
              datasets: [{
                label: 'Stage',
                data: [result['total_lead_stage_new'],result['total_lead_stage_qualified'],result['total_lead_stage_prop']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });


            var ctx = self.$(".total_opportunity_year");
            rpc.query({
                model: "crm.lead",
                method: "get_the_opportunity_year",
            }).then(function (result) {
                self.total_opportunity_stage = result['total_opportunity_stage'],
                self.total_opportunity_stage_new = result['total_opportunity_stage_new'],
                self.total_opportunity_stage_qualified = result['total_opportunity_stage_qualified'],
                self.total_opportunity_stage_prop = result['total_opportunity_stage_prop'],
                self.total_opportunity_stage_won = result['total_opportunity_stage_won'],
                console.log(result,'hgfds')
       const ctx = $('#opportunity_year')

          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: result['total_opportunity_stage'],
              datasets: [{
                label: 'Stage',
                data: [result['total_opportunity_stage_new'],result['total_opportunity_stage_qualified'],result['total_opportunity_stage_prop'],result['total_opportunity_stage_won']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });


            var ctx = self.$(".total_opportunity_month");
            rpc.query({
                model: "crm.lead",
                method: "get_the_opportunity_month",
            }).then(function (result) {
                self.total_opportunity_stage = result['total_opportunity_stage'],
                self.total_opportunity_stage_new = result['total_opportunity_stage_new'],
                self.total_opportunity_stage_qualified = result['total_opportunity_stage_qualified'],
                self.total_opportunity_stage_prop = result['total_opportunity_stage_prop'],
                self.total_opportunity_stage_won = result['total_opportunity_stage_won'],
                console.log(result,'hgfds')
       const ctx = $('#opportunity_month')

          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: result['total_opportunity_stage'],
              datasets: [{
                label: 'Stage',
                data: [result['total_opportunity_stage_new'],result['total_opportunity_stage_qualified'],result['total_opportunity_stage_prop'],result['total_opportunity_stage_won']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });


            var ctx = self.$(".total_opportunity_week");
            rpc.query({
                model: "crm.lead",
                method: "get_the_opportunity_week",
            }).then(function (result) {
                self.total_opportunity_stage = result['total_opportunity_stage'],
                self.total_opportunity_stage_new = result['total_opportunity_stage_new'],
                self.total_opportunity_stage_qualified = result['total_opportunity_stage_qualified'],
                self.total_opportunity_stage_prop = result['total_opportunity_stage_prop'],
                self.total_opportunity_stage_won = result['total_opportunity_stage_won'],
                console.log(result,'hgfds')
       const ctx = $('#opportunity_week')

          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: result['total_opportunity_stage'],
              datasets: [{
                label: 'Stage',
                data: [result['total_opportunity_stage_new'],result['total_opportunity_stage_qualified'],result['total_opportunity_stage_prop'],result['total_opportunity_stage_won']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });


            var ctx = self.$(".total_opportunity_quarter");
            rpc.query({
                model: "crm.lead",
                method: "get_the_opportunity_quarter",
            }).then(function (result) {
                self.total_opportunity_stage = result['total_opportunity_stage'],
                self.total_opportunity_stage_new = result['total_opportunity_stage_new'],
                self.total_opportunity_stage_qualified = result['total_opportunity_stage_qualified'],
                self.total_opportunity_stage_prop = result['total_opportunity_stage_prop'],
                self.total_opportunity_stage_won = result['total_opportunity_stage_won'],
                console.log(result,'hgfds')
       const ctx = $('#opportunity_quarter')

          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: result['total_opportunity_stage'],
              datasets: [{
                label: 'Stage',
                data: [result['total_opportunity_stage_new'],result['total_opportunity_stage_qualified'],result['total_opportunity_stage_prop'],result['total_opportunity_stage_won']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });


            var ctx = self.$(".total_exp_revenue_year");
            rpc.query({
                model: "crm.lead",
                method: "get_total_exp_revenue_year",
            }).then(function (result) {
                self.total_opportunity_stage = result['total_opportunity_stage'],
                self.total_opportunity_exp_stage_new = result['total_opportunity_exp_stage_new'],
                self.total_opportunity_exp_stage_qualified = result['total_opportunity_exp_stage_qualified'],
                self.total_opportunity_exp_stage_prop = result['total_opportunity_exp_stage_prop'],
                self.total_opportunity_exp_stage_won = result['total_opportunity_exp_stage_won'],
                console.log(result,'hgfds')
       const ctx = $('#total_revenue_year')

          new Chart(ctx, {
            type: 'doughnut',
            data: {
              labels: result['total_opportunity_stage'],
              datasets: [{
                label: 'Stage',
                data: [result['total_opportunity_exp_stage_new'],result['total_opportunity_exp_stage_qualified'],result['total_opportunity_exp_stage_prop'],result['total_opportunity_exp_stage_won']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });


            var ctx = self.$(".total_exp_revenue_month");
            rpc.query({
                model: "crm.lead",
                method: "get_total_exp_revenue_month",
            }).then(function (result) {
                self.total_opportunity_stage = result['total_opportunity_stage'],
                self.total_opportunity_exp_stage_new = result['total_opportunity_exp_stage_new'],
                self.total_opportunity_exp_stage_qualified = result['total_opportunity_exp_stage_qualified'],
                self.total_opportunity_exp_stage_prop = result['total_opportunity_exp_stage_prop'],
                self.total_opportunity_exp_stage_won = result['total_opportunity_exp_stage_won'],
                console.log(result,'hgfds')
       const ctx = $('#total_revenue_month')

          new Chart(ctx, {
            type: 'doughnut',
            data: {
              labels: result['total_opportunity_stage'],
              datasets: [{
                label: 'Stage',
                data: [result['total_opportunity_exp_stage_new'],result['total_opportunity_exp_stage_qualified'],result['total_opportunity_exp_stage_prop'],result['total_opportunity_exp_stage_won']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });


            var ctx = self.$(".total_exp_revenue_week");
            rpc.query({
                model: "crm.lead",
                method: "get_total_exp_revenue_week",
            }).then(function (result) {
                self.total_opportunity_stage = result['total_opportunity_stage'],
                self.total_opportunity_exp_stage_new = result['total_opportunity_exp_stage_new'],
                self.total_opportunity_exp_stage_qualified = result['total_opportunity_exp_stage_qualified'],
                self.total_opportunity_exp_stage_prop = result['total_opportunity_exp_stage_prop'],
                self.total_opportunity_exp_stage_won = result['total_opportunity_exp_stage_won'],
                console.log(result,'hgfds')
       const ctx = $('#total_revenue_week')

          new Chart(ctx, {
            type: 'doughnut',
            data: {
              labels: result['total_opportunity_stage'],
              datasets: [{
                label: 'Stage',
                data: [result['total_opportunity_exp_stage_new'],result['total_opportunity_exp_stage_qualified'],result['total_opportunity_exp_stage_prop'],result['total_opportunity_exp_stage_won']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });




            var ctx = self.$(".total_exp_revenue_quarter");
            rpc.query({
                model: "crm.lead",
                method: "get_total_exp_revenue_quarter",
            }).then(function (result) {
                self.total_opportunity_stage = result['total_opportunity_stage'],
                self.total_opportunity_exp_stage_new = result['total_opportunity_exp_stage_new'],
                self.total_opportunity_exp_stage_qualified = result['total_opportunity_exp_stage_qualified'],
                self.total_opportunity_exp_stage_prop = result['total_opportunity_exp_stage_prop'],
                self.total_opportunity_exp_stage_won = result['total_opportunity_exp_stage_won'],
                console.log(result,'hgfds')
       const ctx = $('#total_revenue_quarter')

          new Chart(ctx, {
            type: 'doughnut',
            data: {
              labels: result['total_opportunity_stage'],
              datasets: [{
                label: 'Stage',
                data: [result['total_opportunity_exp_stage_new'],result['total_opportunity_exp_stage_qualified'],result['total_opportunity_exp_stage_prop'],result['total_opportunity_exp_stage_won']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });


            var ctx = self.$(".total_com_revenue_year");
            rpc.query({
                model: "crm.lead",
                method: "get_total_revenue_year",
            }).then(function (result) {
                self.total_opportunity_stage_won = result['total_opportunity_stage_won'],
                self.total_opportunity_exp_stage_others = result['total_opportunity_exp_stage_others'],
                console.log(result,'23456')
       const ctx = $('#total_comp_revenue_year')

          new Chart(ctx, {
            type: 'doughnut',
            data: {
              labels: ['Won', 'Others'],
              datasets: [{
                label: 'Stage',
                data: [result['total_opportunity_stage_won'],result['total_opportunity_exp_stage_others']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });


            var ctx = self.$(".total_com_revenue_month");
            rpc.query({
                model: "crm.lead",
                method: "get_total_revenue_month",
            }).then(function (result) {
                self.total_opportunity_stage_won = result['total_opportunity_stage_won'],
                self.total_opportunity_exp_stage_others = result['total_opportunity_exp_stage_others'],
                console.log(result,'23456')
       const ctx = $('#total_comp_revenue_month')

          new Chart(ctx, {
            type: 'doughnut',
            data: {
              labels: ['Won', 'Others'],
              datasets: [{
                label: 'Stage',
                data: [result['total_opportunity_stage_won'],result['total_opportunity_exp_stage_others']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });


            var ctx = self.$(".total_com_revenue_week");
            rpc.query({
                model: "crm.lead",
                method: "get_total_revenue_week",
            }).then(function (result) {
                self.total_opportunity_stage_won = result['total_opportunity_stage_won'],
                self.total_opportunity_exp_stage_others = result['total_opportunity_exp_stage_others'],
                console.log(result,'23456')
       const ctx = $('#total_comp_revenue_week')

          new Chart(ctx, {
            type: 'doughnut',
            data: {
              labels: ['Won', 'Others'],
              datasets: [{
                label: 'Stage',
                data: [result['total_opportunity_stage_won'],result['total_opportunity_exp_stage_others']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });


            var ctx = self.$(".total_com_revenue_quarter");
            rpc.query({
                model: "crm.lead",
                method: "get_total_revenue_quarter",
            }).then(function (result) {
                self.total_opportunity_stage_won = result['total_opportunity_stage_won'],
                self.total_opportunity_exp_stage_others = result['total_opportunity_exp_stage_others'],
                console.log(result,'23456')
       const ctx = $('#total_comp_revenue_quarter')

          new Chart(ctx, {
            type: 'doughnut',
            data: {
              labels: ['Won', 'Others'],
              datasets: [{
                label: 'Stage',
                data: [result['total_opportunity_stage_won'],result['total_opportunity_exp_stage_others']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });


            var ctx = self.$(".win_ratio_year");
            rpc.query({
                model: "crm.lead",
                method: "get_win_ratio_year",
            }).then(function (result) {
                self.ratio_of_win = result['ratio_of_win'],
                self.ratio_of_lost = result['ratio_of_lost'],
                console.log(result,'23456')
       const ctx = $('#win_ratio_expense_year')

          new Chart(ctx, {
            type: 'pie',
            data: {
              labels: ['Won', 'Lost'],
              datasets: [{
                label: 'Stage',
                data: [result['ratio_of_win'],result['ratio_of_lost']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });



            var ctx = self.$(".win_ratio_month");
            rpc.query({
                model: "crm.lead",
                method: "get_win_ratio_month",
            }).then(function (result) {
                self.ratio_of_win = result['ratio_of_win'],
                self.ratio_of_lost = result['ratio_of_lost'],
                console.log(result,'23456')
       const ctx = $('#win_ratio_expense_month')

          new Chart(ctx, {
            type: 'pie',
            data: {
              labels: ['Won', 'Lost'],
              datasets: [{
                label: 'Stage',
                data: [result['ratio_of_win'],result['ratio_of_lost']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });



            var ctx = self.$(".win_ratio_week");
            rpc.query({
                model: "crm.lead",
                method: "get_win_ratio_week",
            }).then(function (result) {
                self.ratio_of_win = result['ratio_of_win'],
                self.ratio_of_lost = result['ratio_of_lost'],
                console.log(result,'23456')
       const ctx = $('#win_ratio_expense_week')

          new Chart(ctx, {
            type: 'pie',
            data: {
              labels: ['Won', 'Lost'],
              datasets: [{
                label: 'Stage',
                data: [result['ratio_of_win'],result['ratio_of_lost']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });



            var ctx = self.$(".win_ratio_quarter");
            rpc.query({
                model: "crm.lead",
                method: "get_win_ratio_quarter",
            }).then(function (result) {
                self.ratio_of_win = result['ratio_of_win'],
                self.ratio_of_lost = result['ratio_of_lost'],
                console.log(result,'23456')
       const ctx = $('#win_ratio_expense_quarter')

          new Chart(ctx, {
            type: 'pie',
            data: {
              labels: ['Won', 'Lost'],
              datasets: [{
                label: 'Stage',
                data: [result['ratio_of_win'],result['ratio_of_lost']],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
            });

        },
            onclick_this_year: function (ev) {
            var self = this;
            rpc.query({
                model: 'crm.lead',
                method: 'crm_year',
            })
            .then(function (result) {

                         self.$("#activity_week").hide()
                         self.$("#activity_month").hide()
                         self.$("#activity_quarter").hide()

                         self.$("#opportunity_week").hide()
                         self.$("#opportunity_month").hide()
                         self.$("#opportunity_quarter").hide()

                         self.$("#total_revenue_week").hide()
                         self.$("#total_revenue_month").hide()
                         self.$("#total_revenue_quarter").hide()

                         self.$("#total_comp_revenue_week").hide()
                         self.$("#total_comp_revenue_month").hide()
                         self.$("#total_comp_revenue_quarter").hide()

                         self.$("#win_ratio_expense_week").hide()
                         self.$("#win_ratio_expense_month").hide()
                         self.$("#win_ratio_expense_quarter").hide()

            $("#lead_dashboard").empty()
            $("#opportunity_dashboard").empty()
            $("#expected_revenue_dashboard").empty()
            $("#total_revenue_dashboard").empty()
            $("#win_ratio_dashboard").empty()

             $("#lead_dashboard").append('<span>'+result.total_leads_year+'</span>')
             $("#opportunity_dashboard").append('<span>'+result.total_opportunities_year+'</span>')
             $("#expected_revenue_dashboard").append('<span>'+result.total_exp_revenue_year+'</span>')
             $("#total_revenue_dashboard").append('<span>'+result.total_revenue_year+'</span>')
             $("#win_ratio_dashboard").append('<span>'+result.ratio_year+'</span>')


             self.total_leads_year = result['total_leads_year']
             self.total_opportunities_year = result['total_opportunities_year']
             self.total_exp_revenue_year = result['total_exp_revenue_year']
             self.total_revenue_year = result['total_revenue_year']
             self.ratio_year = result['ratio_year']

                                      self.$("#activity_year").show()
                                      self.$("#opportunity_year").show()
                                      self.$("#total_revenue_year").show()
                                      self.$("#total_comp_revenue_year").show()
                                      self.$("#win_ratio_expense_year").show()



            })
            },
           onclick_this_month: function (ev) {
            var self = this;
            rpc.query({
                model: 'crm.lead',
                method: 'crm_month',
            })
            .then(function (result) {

                         self.$("#activity_week").hide()
                         self.$("#activity_year").hide()
                         self.$("#activity_quarter").hide()

                         self.$("#opportunity_week").hide()
                         self.$("#opportunity_year").hide()
                         self.$("#opportunity_quarter").hide()

                         self.$("#total_revenue_week").hide()
                         self.$("#total_revenue_year").hide()
                         self.$("#total_revenue_quarter").hide()

                         self.$("#total_comp_revenue_week").hide()
                         self.$("#total_comp_revenue_year").hide()
                         self.$("#total_comp_revenue_quarter").hide()

                         self.$("#win_ratio_expense_week").hide()
                         self.$("#win_ratio_expense_year").hide()
                         self.$("#win_ratio_expense_quarter").hide()

            $("#lead_dashboard").empty()
            $("#opportunity_dashboard").empty()
            $("#expected_revenue_dashboard").empty()
            $("#total_revenue_dashboard").empty()
            $("#win_ratio_dashboard").empty()

             $("#lead_dashboard").append('<span>'+result.total_leads_month+'</span>')
             $("#opportunity_dashboard").append('<span>'+result.total_opportunities_month+'</span>')
             $("#expected_revenue_dashboard").append('<span>'+result.total_exp_revenue_month+'</span>')
             $("#total_revenue_dashboard").append('<span>'+result.total_revenue_month+'</span>')
             $("#win_ratio_dashboard").append('<span>'+result.ratio_month+'</span>')

             self.total_leads_month = result['total_leads_month']
             self.total_opportunities_month = result['total_opportunities_month']
             self.total_exp_revenue_month = result['total_exp_revenue_month']
             self.total_revenue_month = result['total_revenue_month']
             self.ratio_month = result['ratio_month']

                                      self.$("#activity_month").show()
                                      self.$("#opportunity_month").show()
                                      self.$("#total_revenue_month").show()
                                      self.$("#total_comp_revenue_month").show()
                                      self.$("#win_ratio_expense_month").show()



            })
            },

            onclick_this_week: function (ev) {
            var self = this;
            rpc.query({
                model: 'crm.lead',
                method: 'crm_week',
            })
            .then(function (result) {

                         self.$("#activity_year").hide()
                         self.$("#activity_month").hide()
                         self.$("#activity_quarter").hide()

                         self.$("#opportunity_year").hide()
                         self.$("#opportunity_month").hide()
                         self.$("#opportunity_quarter").hide()

                         self.$("#total_revenue_year").hide()
                         self.$("#total_revenue_month").hide()
                         self.$("#total_revenue_quarter").hide()

                         self.$("#total_comp_revenue_year").hide()
                         self.$("#total_comp_revenue_month").hide()
                         self.$("#total_comp_revenue_quarter").hide()

                         self.$("#win_ratio_expense_year").hide()
                         self.$("#win_ratio_expense_month").hide()
                         self.$("#win_ratio_expense_quarter").hide()


            $("#lead_dashboard").empty()
            $("#opportunity_dashboard").empty()
            $("#expected_revenue_dashboard").empty()
            $("#total_revenue_dashboard").empty()
            $("#win_ratio_dashboard").empty()

             $("#lead_dashboard").append('<span>'+result.total_leads_week+'</span>')
             $("#opportunity_dashboard").append('<span>'+result.total_opportunities_week+'</span>')
             $("#expected_revenue_dashboard").append('<span>'+result.total_exp_revenue_week+'</span>')
             $("#total_revenue_dashboard").append('<span>'+result.total_revenue_week+'</span>')
             $("#win_ratio_dashboard").append('<span>'+result.ratio_week+'</span>')

             self.total_leads_week = result['total_leads_week']
             self.total_opportunities_week = result['total_opportunities_week']
             self.total_exp_revenue_week = result['total_exp_revenue_week']
             self.total_revenue_week = result['total_revenue_week']
             self.ratio_week = result['ratio_week']

                                       self.$("#activity_week").show()
                                       self.$("#opportunity_week").show()
                                       self.$("#total_revenue_week").show()
                                       self.$("#total_comp_revenue_week").show()
                                       self.$("#win_ratio_expense_week").show()


            })
            },

            onclick_this_quarter: function (ev) {
            var self = this;
            rpc.query({
                model: 'crm.lead',
                method: 'crm_quarter',
            })
            .then(function (result) {


                         self.$("#activity_year").hide()
                         self.$("#activity_month").hide()
                         self.$("#activity_week").hide()


                         self.$("#opportunity_year").hide()
                         self.$("#opportunity_month").hide()
                         self.$("#opportunity_week").hide()


                         self.$("#total_revenue_year").hide()
                         self.$("#total_revenue_month").hide()
                         self.$("#total_revenue_week").hide()

                         self.$("#total_comp_revenue_year").hide()
                         self.$("#total_comp_revenue_month").hide()
                         self.$("#total_comp_revenue_week").hide()

                         self.$("#win_ratio_expense_year").hide()
                         self.$("#win_ratio_expense_month").hide()
                         self.$("#win_ratio_expense_week").hide()

            $("#lead_dashboard").empty()
            $("#opportunity_dashboard").empty()
            $("#expected_revenue_dashboard").empty()
            $("#total_revenue_dashboard").empty()
            $("#win_ratio_dashboard").empty()

             $("#lead_dashboard").append('<span>'+result.total_leads_quarter+'</span>')
             $("#opportunity_dashboard").append('<span>'+result.total_opportunities_quarter+'</span>')
             $("#expected_revenue_dashboard").append('<span>'+result.total_exp_revenue_quarter+'</span>')
             $("#total_revenue_dashboard").append('<span>'+result.total_revenue_quarter+'</span>')
             $("#win_ratio_dashboard").append('<span>'+result.ratio_quarter+'</span>')

             self.total_leads_quarter = result['total_leads_quarter']
             self.total_opportunities_quarter = result['total_opportunities_quarter']
             self.total_exp_revenue_quarter = result['total_exp_revenue_quarter']
             self.total_revenue_quarter = result['total_revenue_quarter']
             self.ratio_quarter = result['ratio_quarter']


              self.$("#activity_quarter").show()
              self.$("#opportunity_quarter").show()
              self.$("#total_revenue_quarter").show()
              self.$("#total_comp_revenue_quarter").show()
              self.$("#win_ratio_expense_quarter").show()


            })
            },

})
core.action_registry.add('custom_dashboard', CustomDashBoard);
return CustomDashBoard;
})