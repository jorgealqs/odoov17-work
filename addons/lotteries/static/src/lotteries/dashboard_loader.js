/** @odoo-module */

import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { Component, xml } from "@odoo/owl";

class DashboardGamesLoader extends Component {
    static components = { LazyComponent };
    static template = xml`
    <LazyComponent bundle="'lotteries.dashboard'" Component="'DashboardGamesLottery'" props="props"/>
    `;
}

registry.category("actions").add("lotteries.dashboardAction", DashboardGamesLoader);