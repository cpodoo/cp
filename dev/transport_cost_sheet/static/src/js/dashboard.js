/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class TransportDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.totalSheets = 0;

        onWillStart(async () => {
            const result = await this.orm.call("transport.cost.sheet", "get_dashboard_data", []);
            this.totalSheets = result.total_cost_sheets;
        });
    }
}

TransportDashboard.template = "transport_cost_sheet.TransportDashboard";

registry.category("actions").add("transport_dashboard_tag", TransportDashboard);
