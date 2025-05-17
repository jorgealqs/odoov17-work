/** @odoo-module **/

import { Component } from  "@odoo/owl";


export class DashboardButtons extends Component {
    static template = "sports_sync_data.ButtonsSports";
    static props = {
        buttons: Object,
        onClickModel: Function,
    }

    onClick(ev) {
        const model = ev.target.dataset.model;
        this.props.onClickModel(model)
    }

}