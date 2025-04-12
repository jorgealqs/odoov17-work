/** @odoo-module */

import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { Component, xml } from "@odoo/owl";

class ForescastLoader extends Component {
    static components = { LazyComponent };
    static template = xml`
    <LazyComponent bundle="'lotteries.forecast'" Component="'ForescastGames'" props="props"/>
    `;
}

registry.category("actions").add("lotteries.forecastAction", ForescastLoader);