/** @odoo-module */

import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { Component, xml } from "@odoo/owl";

class DashboardLazySportsSyncData extends Component {
    static components = { LazyComponent };
    static template = xml`
    <LazyComponent bundle="'sports_sync_data.dashboard'" Component="'DashboardSportsSync'" props="props"/>
    `;
}

registry.category("actions").add("sports_data_sync.DashboardActionSportsSyncData", DashboardLazySportsSyncData);