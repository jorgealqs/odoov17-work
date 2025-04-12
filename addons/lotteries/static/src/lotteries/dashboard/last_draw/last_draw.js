/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardLastDraw extends Component {
    static template = "lotteries.DashboardLastDraw";
    static props = {
        lastDraw: Array,
    };

}