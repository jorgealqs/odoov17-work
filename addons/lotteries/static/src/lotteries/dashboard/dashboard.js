/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { DashboardLastDraw } from "./last_draw/last_draw";

class DashboardGames extends Component {
    static template = "lotteries.Dashboard";
    static components = { Layout, DashboardItem, PieChart, DashboardLastDraw };

    setup() {
        this.action = useService("action");
        this.rpc = useService("rpc");
        this.display = {
            controlPanel: {},
        };
        this.statistics = useState(useService("lotteries.statistics"));
        console.log(this.statistics);
    }

    openLotteriesDraws(){
        this.action.doAction("lotteries.action_lottery_draw");
    }

}

registry.category("lazy_components").add("DashboardGames", DashboardGames);