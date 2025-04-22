/** @odoo-module */

import { Component, useRef } from "@odoo/owl"

export class MatchesSportsSyncData extends Component {
    static template = "sports_sync_data.Games"
    static props = {
        data: {
            type: Object,
        }
    }
}