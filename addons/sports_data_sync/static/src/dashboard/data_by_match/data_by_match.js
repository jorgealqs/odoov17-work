/** @odoo-module **/

import { Component } from  "@odoo/owl";


export class DashboardDataByMatch extends Component {
    static template = "sports_sync_data.DataByMatch";
    static props = {
        data: Object
    }
}