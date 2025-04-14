/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardLastDraw extends Component {
    static template = "lotteries.DashboardLastItemDraw";
    static props = {
        lastDraw: { type: Object },
    };

    setup() {
        console.log(this.props.lastDraw);
    }

}