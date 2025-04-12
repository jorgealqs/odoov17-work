/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class SelectGame extends Component {
    static template = "lotteries.SelectGame";
    static props = {
        title: {
            type: String,
            optional: true,
            default: "Lottery Game"
        },
        games: Array,
        name: String,
        onSelectChange: Function,
    };

    onSelectChange(ev) {
        const selectedValue = ev.target.value;
        this.props.onSelectChange({ title: this.props.title, value: selectedValue });
    }

}