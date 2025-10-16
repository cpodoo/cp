/** @odoo-module */
import { registry } from '@web/core/registry';
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { onMounted, onPatched, onWillUnmount, useEffect, useRef } from "@odoo/owl";

// import { jsonrpc } from "@web/core/network/rpc_service";
import { _t } from "@web/core/l10n/translation";
import { loadJS } from "@web/core/assets";
import { Component, onWillStart, onWillUpdateProps, useState } from "@odoo/owl";

export class CourierDashboard extends Component {

    setup() {
        this.action = useService("action");
        this.orm = useService("orm");
        this.rpc = this.env.services.rpc
        onWillStart(this.onWillStart);
        onMounted(this.onMounted);
    }

    async onWillStart() {
        // MIGRATED
       await this.fetch_data();
       await this.getGreetings()
       await loadJS("https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.9.2/html2pdf.bundle.min.js")
       // await loadJS("https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js")
    }

    async onMounted() {
        // MIGRATED
       this.render_courier_chart_data();
       this.render_courier_filter();
    //    this._onchangeStateChart();
    //    this._onchangeCountryChart();
    //    this._onchangeTypeChart();
    //    this._onchangeStateChart();
    }

    async getGreetings() {
        var self = this;
        const now = new Date();
        const hours = now.getHours();
        if (hours >= 5 && hours < 12) {
            self.greetings = "Good Morning";
        }
        else if (hours >= 12 && hours < 18) {
            self.greetings = "Good Afternoon";
        }
        else {
            self.greetings = "Good Evening";
        }
    }

    // -------Print CourierDashboard---------

    downloadReport(e) {
        e.stopPropagation();
        e.preventDefault();
        var opt = {
            margin: 1,
            filename: 'CourierDashboard.pdf',
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'px', format: [1920, 1080], orientation: 'landscape' }
        };
        html2pdf().set(opt).from(document.getElementById("dashboard")).save()
    }

    // ---------------Download Chart-----------------

    _downloadChart(e) {
        const chart = e.target.offsetParent.children[2].children[0]; // Get the chart canvas element
        const imageDataURL = chart.toDataURL('image/png'); // Generate image data URL
        const filename = chart.id+'CourierDashboard.png'; // Set your preferred filename
        const link = document.createElement('a');
        link.href = imageDataURL;
        link.download = filename;
        link.click();
    }

    async render_courier_chart_data() {
        // MIGRATED
        
        var user_selectionss = document.querySelector('#user_selections')?.value;
        var partner_selection = document.querySelector('#partner_selection')?.value;
        var priority_selection = document.querySelector('#priority_selection')?.value;
        var duration_selection = document.querySelector('#duration_selection')?.value;
        // var all_order_range_selection = document.querySelector('#all_order_range_selection')?.value;
        var delivery_state_range_selection = document.querySelector('#delivery_state_range_selection')?.value;
        var delivery_country_range_selection = document.querySelector('#delivery_country_range_selection')?.value;
        var delivery_type_range_selection = document.querySelector('#delivery_type_range_selection')?.value;

        var self = this;

        await rpc("/courier/chart/data", {
            'data': {
                
                'user_id': user_selectionss,
                'partner_id': partner_selection,
                'priority_id': priority_selection,
                'duration':duration_selection,
                // 'all_order_range_selection':all_order_range_selection,
                'delivery_state_range_selection': delivery_state_range_selection,
                'delivery_country_range_selection': delivery_country_range_selection,
                'delivery_type_range_selection': delivery_type_range_selection,

            }
        }).then(function (data) {
            var ctx = document.querySelector("#all_stage_chart_data");
            new Chart(ctx, {
                type: document.querySelector('#all_stage_chart_selection')?.value,
                data: data.all_stage_chart_data,
                options: {
                    maintainAspectRatio: false,
                }
            });

            var ctx = document.querySelector("#delivery_state_chart_data");
            new Chart(ctx, {
                type: document.querySelector('#delivery_state_chart_selection')?.value,
                data: data.delivery_state_chart_data,
                options: {
                    maintainAspectRatio: false,
                }
            });

            var ctx = document.querySelector("#delivery_country_chart_data");
            new Chart(ctx, {
                type: document.querySelector('#delivery_country_chart_selection')?.value,
                data: data.delivery_country_chart_data,
                options: {
                    maintainAspectRatio: false
                }
            });

            var ctx = document.querySelector("#delivery_type_chart_data");
            new Chart(ctx, {
                type: document.querySelector('#delivery_type_chart_selection')?.value,
                data: data.delivery_type_chart_data,
                options: {
                    maintainAspectRatio: false
                }
            });

            // List View----------------------------
            
            var all_collected_list = data['all_collected_list'];
            var tbody = document.querySelector("#my_table_all_collected_list tbody");
            tbody.innerHTML = '';
            for (var i = 0; i < all_collected_list.length; i++) {
                // Create a new row
                var row = document.createElement("tr");
                // Create cells for each property in the object
                for (var key in all_collected_list[i]) {
                    if (key !== 'id') {
                        var cell = document.createElement("td");
                        if (all_collected_list[i][key].length == 2) {
                            cell.textContent = all_collected_list[i][key][1];
                            row.appendChild(cell);
                        }
                        else if(key==='registration_date')
                        {
                            var cell = document.createElement("td");
                            var registration_date=all_collected_list[i]['registration_date']
                            if(registration_date)
                            {
                                 var arr1 = registration_date.split('-');
                                 cell.textContent = arr1[2] + '-' + arr1[1] + '-' + arr1[0];
                             }
                             else
                             {
                                cell.textContent='-'
                             }
                             row.appendChild(cell);
                        }
                        else if(key==='delivery_date')
                        {
                            var cell = document.createElement("td");
                            var delivery_date=all_collected_list[i]['delivery_date']
                            if (delivery_date)
                            {
                                var arr1 = delivery_date.split('-');
                                cell.textContent =  arr1[2] + '-' + arr1[1] + '-' + arr1[0];
                            }
                            else
                            {
                                cell.textContent = '-'
                            }
                            row.appendChild(cell);
                        }
 
                        else {
                            if (all_collected_list[i][key] == false) {
                                cell.textContent = ' ';
                                row.appendChild(cell);
                            } else {
                                cell.textContent = all_collected_list[i][key];
                                row.appendChild(cell);
                            }
                        }

                    }
                }
            var buttonCell = document.createElement("td");
    		var button = document.createElement("button");
    		button.textContent = "View";
    		button.setAttribute("data-id", all_collected_list[i].id);
    		button.addEventListener("click", function() {
		    var id = this.getAttribute("data-id");
				// Call your function with the ID
				collected_tree_button_function(id);
			});
    		button.style.backgroundColor = "Pink";
    		button.style.color = "black";
    		button.style.padding = "10px 16px";
    		buttonCell.appendChild(button);
    		row.appendChild(buttonCell);
            tbody.appendChild(row);
            }
            
        	function collected_tree_button_function(id) {
				var options = {
				};
				self.action.doAction({
				    name: _t("Collected"),
				    type: 'ir.actions.act_window',
				    res_model: 'dev.courier.request',
				    domain: [["id", "=", id]],
				    view_mode: 'list,form',
				    views: [
				        [false, 'list'],
				        [false, 'form']
				    ],
				    target: 'current'
				}, options)
			}

            var all_transit_list = data['all_transit_list'];
            var tbody = document.querySelector("#my_table_all_transit_list tbody");
            tbody.innerHTML = '';
            for (var i = 0; i < all_transit_list.length; i++) {
                // Create a new row
                var row = document.createElement("tr");
                // Create cells for each property in the object
                for (var key in all_transit_list[i]) {
                    if (key !== 'id') {
                        var cell = document.createElement("td");
                        if (all_transit_list[i][key].length == 2) {
                            cell.textContent = all_transit_list[i][key][1];
                            row.appendChild(cell);
                        } 
                        else if(key==='registration_date')
                        {
                            var cell = document.createElement("td");
                            var registration_date=all_transit_list[i]['registration_date']
                            if(registration_date)
                            {
                                 var arr1 = registration_date.split('-');
                                 cell.textContent = arr1[2] + '-' + arr1[1] + '-' + arr1[0];
                             }
                             else
                             {
                                cell.textContent='-'
                             }
                             row.appendChild(cell);
                        }
                        else if(key==='delivery_date')
                        {
                            var cell = document.createElement("td");
                            var delivery_date=all_transit_list[i]['delivery_date']
                            if (delivery_date)
                            {
                                var arr1 = delivery_date.split('-');
                                cell.textContent =  arr1[2] + '-' + arr1[1] + '-' + arr1[0];
                            }
                            else
                            {
                                cell.textContent = '-'
                            }
                            row.appendChild(cell);
                        }
                        else {
                            if (all_transit_list[i][key] == false) {
                                cell.textContent = ' ';
                                row.appendChild(cell);
                            } else {
                                cell.textContent = all_transit_list[i][key];
                                row.appendChild(cell);
                            }
                        }

                    }
                }
            var buttonCell = document.createElement("td");
    		var button = document.createElement("button");
    		button.textContent = "View";
    		button.setAttribute("data-id", all_transit_list[i].id);
    		button.addEventListener("click", function() {
		    var id = this.getAttribute("data-id");
				// Call your function with the ID
				transit_tree_button_function(id);
			});
    		button.style.backgroundColor = "Pink";
    		button.style.color = "black";
    		button.style.padding = "10px 16px";
    		buttonCell.appendChild(button);
    		row.appendChild(buttonCell);
            tbody.appendChild(row);
            }
            
        	function transit_tree_button_function(id) {
				var options = {
				};
				self.action.doAction({
				    name: _t("Transit"),
				    type: 'ir.actions.act_window',
				    res_model: 'dev.courier.request',
				    domain: [["id", "=", id]],
				    view_mode: 'list,form',
				    views: [
				        [false, 'list'],
				        [false, 'form']
				    ],
				    target: 'current'
				}, options)
			}

            var all_delivered_list = data['all_delivered_list'];
            var tbody = document.querySelector("#my_table_all_delivered_list tbody");
            tbody.innerHTML = '';
            for (var i = 0; i < all_delivered_list.length; i++) {
                // Create a new row
                var row = document.createElement("tr");
                // Create cells for each property in the object
                for (var key in all_delivered_list[i]) {
                    if (key !== 'id') {
                        var cell = document.createElement("td");
                        if (all_delivered_list[i][key].length == 2) {
                            cell.textContent = all_delivered_list[i][key][1];
                            row.appendChild(cell);
                        } 
                        else if(key==='registration_date')
                        {
                            var cell = document.createElement("td");
                            var registration_date=all_delivered_list[i]['registration_date']
                            if(registration_date)
                            {
                                 var arr1 = registration_date.split('-');
                                 cell.textContent = arr1[2] + '-' + arr1[1] + '-' + arr1[0];
                             }
                             else
                             {
                                cell.textContent='-'
                             }
                             row.appendChild(cell);
                        }
                        else if(key==='delivery_date')
                        {
                            var cell = document.createElement("td");
                            var delivery_date=all_delivered_list[i]['delivery_date']
                            if (delivery_date)
                            {
                                var arr1 = delivery_date.split('-');
                                cell.textContent =  arr1[2] + '-' + arr1[1] + '-' + arr1[0];
                            }
                            else
                            {
                                cell.textContent = '-'
                            }
                            row.appendChild(cell);
                        }
                        else {
                            if (all_delivered_list[i][key] == false) {
                                cell.textContent = ' ';
                                row.appendChild(cell);
                            } else {
                                cell.textContent = all_delivered_list[i][key];
                                row.appendChild(cell);
                            }
                        }

                    }
                }
            var buttonCell = document.createElement("td");
    		var button = document.createElement("button");
    		button.textContent = "View";
    		button.setAttribute("data-id", all_delivered_list[i].id);
    		button.addEventListener("click", function() {
		    var id = this.getAttribute("data-id");
				// Call your function with the ID
				delivered_tree_button_function(id);
			});
    		button.style.backgroundColor = "Pink";
    		button.style.color = "black";
    		button.style.padding = "10px 16px";
    		buttonCell.appendChild(button);
    		row.appendChild(buttonCell);
            tbody.appendChild(row);
            }
            
        	function delivered_tree_button_function(id) {
				var options = {
				};
				self.action.doAction({
				    name: _t("Delivered"),
				    type: 'ir.actions.act_window',
				    res_model: 'dev.courier.request',
				    domain: [["id", "=", id]],
				    view_mode: 'list,form',
				    views: [
				        [false, 'list'],
				        [false, 'form']
				    ],
				    target: 'current'
				}, options)
			}

            var all_cancel_list = data['all_cancel_list'];
            var tbody = document.querySelector("#my_table_all_cancel_list tbody");
            tbody.innerHTML = '';
            for (var i = 0; i < all_cancel_list.length; i++) {
                // Create a new row
                var row = document.createElement("tr");
                // Create cells for each property in the object
                for (var key in all_cancel_list[i]) {
                    if (key !== 'id') {
                        var cell = document.createElement("td");
                        if (all_cancel_list[i][key].length == 2) {
                            cell.textContent = all_cancel_list[i][key][1];
                            row.appendChild(cell);
                        } 
                        else if(key==='registration_date')
                        {
                            var cell = document.createElement("td");
                            var registration_date=all_cancel_list[i]['registration_date']
                            if(registration_date)
                            {
                                 var arr1 = registration_date.split('-');
                                 cell.textContent = arr1[2] + '-' + arr1[1] + '-' + arr1[0];
                             }
                             else
                             {
                                cell.textContent='-'
                             }
                             row.appendChild(cell);
                        }
                        else if(key==='delivery_date')
                        {
                            var cell = document.createElement("td");
                            var delivery_date=all_cancel_list[i]['delivery_date']
                            if (delivery_date)
                            {
                                var arr1 = delivery_date.split('-');
                                cell.textContent =  arr1[2] + '-' + arr1[1] + '-' + arr1[0];
                            }
                            else
                            {
                                cell.textContent = '-'
                            }
                            row.appendChild(cell);
                        }
                        else {
                            if (all_cancel_list[i][key] == false) {
                                cell.textContent = ' ';
                                row.appendChild(cell);
                            } else {
                                cell.textContent = all_cancel_list[i][key];
                                row.appendChild(cell);
                            }
                        }

                    }
                }
            var buttonCell = document.createElement("td");
    		var button = document.createElement("button");
    		button.textContent = "View";
    		button.setAttribute("data-id", all_cancel_list[i].id);
    		button.addEventListener("click", function() {
		    var id = this.getAttribute("data-id");
				// Call your function with the ID
				cancel_tree_button_function(id);
			});
    		button.style.backgroundColor = "Pink";
    		button.style.color = "black";
    		button.style.padding = "10px 16px";
    		buttonCell.appendChild(button);
    		row.appendChild(buttonCell);
            tbody.appendChild(row);
            }
            
        	function cancel_tree_button_function(id) {
				var options = {
				};
				self.action.doAction({
				    name: _t("Cancel"),
				    type: 'ir.actions.act_window',
				    res_model: 'dev.courier.request',
				    domain: [["id", "=", id]],
				    view_mode: 'list,form',
				    views: [
				        [false, 'list'],
				        [false, 'form']
				    ],
				    target: 'current'
				}, options)
			}

        })
    }

    // Filter-------------------------------

    // render_courier_filter() {
    //     rpc('/all_courier_filter').then(function (data) {
    //         var users = data[0]
    //         var partners = data[1]
    //         var prioritys = data[2]
    //         var durations=data[3]
    //         // var today = new Date();

    //         // $(users).each(function (user) {
    //         //     $('#user_selections').append("<option value=" + users[user].id + ">" + users[user].name + "</option>");
    //         // });
    //         // $(partners).each(function (partner) {
    //         //     $('#partner_selection').append("<option value=" + partners[partner].id + ">" + partners[partner].name + "</option>");
    //         // });
    //         // $(prioritys).each(function (priority) {
    //         //     $('#priority_selection').append("<option value=" + prioritys[priority].id + ">" + prioritys[priority].name + "</option>");
    //         // });
    //         // $(durations).each(function (duration) {
    //         //     $('#duration_selection').append("<option value=" + durations[duration].id + ">" + durations[duration].name + "</option>");
    //         // });

    //         const userSelect     = document.querySelector("#user_selections");
    //         const partnerSelect  = document.querySelector("#partner_selection");
    //         const prioritySelect = document.querySelector("#priority_selection");
    //         const durationSelect = document.querySelector("#duration_selection");
    //         function fillOptions(list, selectEl) {
    //             // clear existing options, if you want
    //             selectEl.innerHTML = "";
    //             list.forEach(item => {
    //                 const opt = document.createElement("option");
    //                 opt.value       = item.id;
    //                 opt.textContent = item.name;
    //                 selectEl.appendChild(opt);
    //             });
    //         }
    //         fillOptions(users,     userSelect);
    //         fillOptions(partners,  partnerSelect);
    //         fillOptions(prioritys,  prioritySelect);
    //         fillOptions(durations, durationSelect);
    //     })
    // }
    render_courier_filter() {
        rpc('/all_courier_filter').then((data) => {
            const users     = data[0] || [];
            const partners  = data[1] || [];
            const prioritys = data[2] || [];
            const durations = data[3] || [];

            const userSelect     = document.querySelector("#user_selections");
            const partnerSelect  = document.querySelector("#partner_selection");
            const prioritySelect = document.querySelector("#priority_selection");
            const durationSelect = document.querySelector("#duration_selection");

            function fillOptions(list, selectEl) {
                if (!Array.isArray(list) || !selectEl) return;
                // selectEl.innerHTML = "";
                list.forEach(item => {
                    const opt = document.createElement("option");
                    opt.value = item.id;
                    opt.textContent = item.name;
                    selectEl.appendChild(opt);
                });
            }

            fillOptions(users, userSelect);
            fillOptions(partners, partnerSelect);
            fillOptions(prioritys, prioritySelect);
            fillOptions(durations, durationSelect);
        });
    }

    
    
    
    _onchangeCourierFilter(ev) {
        this.flag = 1
        
        var user_selectionss = document.querySelector('#user_selections')?.value;
        var partner_selection = document.querySelector('#partner_selection')?.value;
        var priority_selection = document.querySelector('#priority_selection')?.value;
        var duration_selection = document.querySelector('#duration_selection')?.value;

        this.render_courier_chart_data();
        var self = this;
        
        rpc('/courier/filter-apply', {
            'data': {
                'user': user_selectionss,
                'partner': partner_selection,
                'priority': priority_selection,
                'duration': duration_selection,
            }
        }).then(function (data) {

            		    // count box click that time pass data
            self.new_data = data['new_data']
            self.collected_data = data['collected_data']
            self.dispatched_data = data['dispatched_data']
            self.intransit_data = data['intransit_data']
            self.out_of_delivery_data = data['out_of_delivery_data']
            self.delivered_data = data['delivered_data']
            self.cancel_data = data['cancel_data']
            self.all_invoice_ids = data['all_invoice_ids']
            


			// after change value display on xml side count
            document.getElementById('new_data').innerHTML = data['new_data'].length;
            document.getElementById('collected_data').innerHTML = data['collected_data'].length;
            document.getElementById('dispatched_data').innerHTML = data['dispatched_data'].length;
            document.getElementById('intransit_data').innerHTML = data['intransit_data'].length;
            document.getElementById('out_of_delivery_data').innerHTML = data['out_of_delivery_data'].length;
            document.getElementById('delivered_data').innerHTML = data['delivered_data'].length;
            document.getElementById('cancel_data').innerHTML = data['cancel_data'].length;
            document.getElementById('all_invoice_ids').innerHTML = data['all_invoice_ids'].length;

        })
    }

    
    async _onchangeStatusChart(ev)
    {
        var user_selectionss = document.querySelector('#user_selections')?.value;
        var partner_selection = document.querySelector('#partner_selection')?.value;
        var priority_selection = document.querySelector('#priority_selection')?.value;
        var duration_selection = document.querySelector('#duration_selection')?.value;

        var all_stage_chart_selection = document.querySelector('#all_stage_chart_selection')?.value;
        // var all_order_range_selection=$('#all_order_range_selection').val();
        var self = this;
        await rpc("/courier/status/chart/data",
        {
        'data':
            {
                'user_id': user_selectionss,
                'partner_id': partner_selection,
                'priority_id': priority_selection,
                'duration':duration_selection,
                // 'all_order_range_selection':all_order_range_selection,
            }
        }).then(function (data)
        {
            // var ctx = $("#all_stage_chart_data");
            const canvas = document.getElementById('all_stage_chart_data');
            const ctx = canvas?.getContext('2d');

            new Chart(ctx, {
                type: all_stage_chart_selection,
                data: data.all_stage_chart_data,
                options: {
                    maintainAspectRatio: false,

                    onClick: (evt, elements) => {
                        if (elements.length > 0) {
                            const element = elements[0];
                            const clickedIndex = element.index;
                            const clickedLabel = data.all_stage_chart_data.labels[clickedIndex];
                            const clickedValue = data.all_stage_chart_data.datasets[0].detail[clickedIndex]
//                            console.log("Clicked label:", clickedLabel, "Clicked value:", clickedValue);
                            var options = {
                            };
                            self.action.doAction({
                                name: _t(clickedLabel),
                                type: 'ir.actions.act_window',
                                res_model: 'dev.courier.request',
                                domain: [["id", "in", clickedValue]],
                                view_mode: 'list,form',
                                views: [
                                    [false, 'list'],
                                    [false, 'form']
                                ],
                                target: 'current'
                            }, options)
                        } else {
//                            console.log("Click outside chart area");
                        }
                    }
                }
            });
        });
    }

    async _onchangeStateChart(ev) 
    {
        var user_selectionss = document.querySelector('#user_selections')?.value;
        var partner_selection = document.querySelector('#partner_selection')?.value;
        var priority_selection = document.querySelector('#priority_selection')?.value;
        var duration_selection = document.querySelector('#duration_selection')?.value;
        var delivery_state_chart_selection = document.querySelector('#delivery_state_chart_selection')?.value;
        var delivery_state_range_selection = document.querySelector('#delivery_state_range_selection')?.value;

        var self = this;

        await rpc("/courier/state/chart/data", {
            'data': {
                
                'user_id': user_selectionss,
                'partner_id': partner_selection,
                'priority_id': priority_selection,
                'duration':duration_selection,
                'delivery_state_range_selection':delivery_state_range_selection,
            }
        }).then(function (data) {
            const canvas = document.getElementById('delivery_state_chart_data');
            const ctx = canvas?.getContext('2d');
            // var ctx = $("#delivery_state_chart_data");
            new Chart(ctx, {
                type: delivery_state_chart_selection,
                data: data.delivery_state_chart_data,
                options: {
                    maintainAspectRatio: false,

                    onClick: (evt, elements) => {
                        if (elements.length > 0) {
                            const element = elements[0];
                            const clickedIndex = element.index;
                            const clickedLabel = data.delivery_state_chart_data.labels[clickedIndex];
                            const clickedValue = data.delivery_state_chart_data.datasets[0].detail[clickedIndex]
                            // console.log("Clicked label:", clickedLabel, "Clicked value:", clickedValue);
                            var options = {
                            };
                            self.action.doAction({
                                name: _t(clickedLabel),
                                type: 'ir.actions.act_window',
                                res_model: 'dev.courier.request',
                                domain: [["id", "in", clickedValue]],
                                view_mode: 'list,form',
                                views: [
                                    [false, 'list'],
                                    [false, 'form']
                                ],
                                target: 'current'
                            }, options)
                        } else {
//                            console.log("Click outside chart area");
                        }
                    }
                }
            });
        });
    
    }
    
   
    async _onchangeCountryChart(ev)
    {
        var user_selectionss = document.querySelector('#user_selections')?.value;
        var partner_selection = document.querySelector('#partner_selection')?.value;
        var priority_selection = document.querySelector('#priority_selection')?.value;
        var duration_selection = document.querySelector('#duration_selection')?.value;
        var delivery_country_chart_selection = document.querySelector('#delivery_country_chart_selection')?.value;
        var delivery_country_range_selection = document.querySelector('#delivery_country_range_selection')?.value;
        var self = this;
        await rpc("/courier/country/chart/data",
        {
        'data':
            {
                'user_id': user_selectionss,
                'partner_id': partner_selection,
                'priority_id': priority_selection,
                'duration':duration_selection,
                'delivery_country_range_selection': delivery_country_range_selection,
            }
        }).then(function (data)
        {   const canvas = document.getElementById('delivery_country_chart_data');
const       ctx = canvas?.getContext('2d');
            // var ctx = $("#delivery_country_chart_data");
            new Chart(ctx, {
                type: delivery_country_chart_selection,
                data: data.delivery_country_chart_data,
                options: {
                    maintainAspectRatio: false,

                    onClick: (evt, elements) => {
                        if (elements.length > 0) {
                            const element = elements[0];
                            const clickedIndex = element.index;
                            const clickedLabel = data.delivery_country_chart_data.labels[clickedIndex];
                            const clickedValue = data.delivery_country_chart_data.datasets[0].detail[clickedIndex]
//                            console.log("Clicked label:", clickedLabel, "Clicked value:", 10);
                            var options = {
                            };
                            self.action.doAction({
                                name: _t(clickedLabel),
                                type: 'ir.actions.act_window',
                                res_model: 'dev.courier.request',
                                domain: [["id", "in", clickedValue]],
                                view_mode: 'list,form',
                                views: [
                                    [false, 'list'],
                                    [false, 'form']
                                ],
                                target: 'current'
                            }, options)
                        } else {
//                            console.log("Click outside chart area");
                        }
                    }
                }
            });
        });
    }

    async _onchangeTypeChart(ev)
    {
        var user_selectionss = document.querySelector('#user_selections')?.value;
        var partner_selection = document.querySelector('#partner_selection')?.value;
        var priority_selection = document.querySelector('#priority_selection')?.value;
        var duration_selection = document.querySelector('#duration_selection')?.value;
        var delivery_type_chart_selection = document.querySelector('#delivery_type_chart_selection')?.value;
        var delivery_type_range_selection = document.querySelector('#delivery_type_range_selection')?.value;
        var self = this;
        await rpc("/courier/type/chart/data",
        {
        'data':
            {
                'user_id': user_selectionss,
                'partner_id': partner_selection,
                'priority_id': priority_selection,
                'duration':duration_selection,
                'delivery_type_range_selection': delivery_type_range_selection,
            }
        }).then(function (data)
        {   
            const canvas = document.getElementById('delivery_type_chart_data');
            const ctx = canvas?.getContext('2d');
            // var ctx = $("#delivery_type_chart_data");
            new Chart(ctx, {
                type: delivery_type_chart_selection,
                data: data.delivery_type_chart_data,
                options: {
                    maintainAspectRatio: false,

                    onClick: (evt, elements) => {
                        if (elements.length > 0) {
                            const element = elements[0];
                            const clickedIndex = element.index;
                            const clickedLabel = data.delivery_type_chart_data.labels[clickedIndex];
                            const clickedValue = data.delivery_type_chart_data.datasets[0].detail[clickedIndex]
//                            console.log("Clicked label:", clickedLabel, "Clicked value:", 10);
                            var options = {
                            };
                            self.action.doAction({
                                name: _t(clickedLabel),
                                type: 'ir.actions.act_window',
                                res_model: 'dev.courier.request',
                                domain: [["id", "in", clickedValue]],
                                view_mode: 'list,form',
                                views: [
                                    [false, 'list'],
                                    [false, 'form']
                                ],
                                target: 'current'
                            }, options)
                        } else {
//                            console.log("Click outside chart area");
                        }
                    }
                }
            });
        });
    }


    fetch_data() {
        this.flag = 0;
        return rpc('/get/courier/tiles/data', {}).then((result) => {
            this.new_data = result.new_data;
            this.collected_data = result.collected_data;
            this.dispatched_data = result.dispatched_data;
            this.intransit_data = result.intransit_data;
            this.out_of_delivery_data = result.out_of_delivery_data;
            this.delivered_data = result.delivered_data;
            this.cancel_data = result.cancel_data;
            this.all_invoice_ids = result.all_invoice_ids;
            this.user_name = result.user_name;
            this.user_img = result.user_img;
        });
    }

    action_new(e) {
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        //		if (this.flag == 0) {
        const rec_id = e.currentTarget.querySelector('[rec-id]')?.getAttribute('rec-id');
        const action = e.currentTarget.querySelector('[rec-id]')?.id || false;
        var domain = false;

        if (action == 'new_data') {
            domain = [["id", "in", this.new_data]];
        } else if (action == 'collected_data') {
            domain = [["id", "in", this.collected_data]]
        } else if (action == 'dispatched_data') {
            domain = [["id", "in", this.dispatched_data]]
        } else if (action == 'intransit_data') {
            domain = [["id", "in", this.intransit_data]]
        } else if (action == 'out_of_delivery_data') {
            domain = [["id", "in", this.out_of_delivery_data]]
        } else if (action == 'delivered_data') {
            domain = [["id", "in", this.delivered_data]]
        } else if (action == 'cancel_data') {
            domain = [["id", "in", this.cancel_data]]
        } else if (rec_id != undefined) {
            domain = [["id", "=", rec_id]]
        }
        
        this.action.doAction({
            name: _t(" All Data"),
            type: 'ir.actions.act_window',
            res_model: 'dev.courier.request',
            domain: domain,
            view_mode: 'list,form',
            views: [
                [false, 'list'],
                [false, 'form']
            ],
            target: 'current'
        }, options)
    }

    action_all_invoices(e) {
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        const action = e.currentTarget.children[0]?.children[0]?.id || false;
        var domain = false;

        if (action == 'all_invoice_ids') {
            domain = [["id", "in", this.all_invoice_ids]];
        } 

        this.action.doAction({
            name: _t("Invoices"),
            type: 'ir.actions.act_window',
            res_model: 'account.move',
            domain: domain,
            view_mode: 'list,form',
            views: [
                [false, 'list'],
                [false, 'form']
            ],
            target: 'current'
        }, options)
    }

}                          
CourierDashboard.template = "courierdashboard"
registry.category("actions").add("courier_dashboard", CourierDashboard)
