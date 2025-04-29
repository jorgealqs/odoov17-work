/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardLastDraw extends Component {
    static template = "lotteries.DashboardLastItemDraw";
    static props = {
        lastDraw: { type: Object },
        onClickGame: {
            type: Object
        }
    };

    onClickGame(ev){
        const drawId = ev.currentTarget.dataset.id;
        const lottery = ev.currentTarget.dataset.lottery;
        this.props.onClickGame(drawId, lottery);
    }

}