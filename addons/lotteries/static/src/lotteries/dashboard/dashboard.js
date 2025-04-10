/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";

class DashboardGames extends Component {
    static template = "lotteries.Dashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.rpc = useService("rpc");
        this.display = {
            controlPanel: {},
        };
        this.statistics = useState(useService("lotteries.statistics"));
    }

    openLotteriesDraws(){
        this.action.doAction("lotteries.action_lottery_draw");
    }

}

registry.category("lazy_components").add("DashboardGames", DashboardGames);