/** @odoo-module */

import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { Component, xml } from "@odoo/owl";

class DashboardGamesSports extends Component {
    static components = { LazyComponent };
    static template = xml`
    <LazyComponent bundle="'sports_betting.dashboard'" Component="'DashboardSports'" props="props"/>
    `;
}

registry.category("actions").add("sports_betting.dashboardActionSports", DashboardGamesSports);