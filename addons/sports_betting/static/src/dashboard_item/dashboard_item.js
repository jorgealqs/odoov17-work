/** @odoo-module */

import { Component } from "@odoo/owl";

export class DashboardItemSports extends Component {
    static template = "awesome_dashboard.DashboardItemSports"
    static props = {
        slots: {
            type: Object,
            shape: {
                default: Object
            },
        },
        size: {
            type: Number,
            default: 1,
            optional: true,
        },
    };
}