/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItemSports } from "../dashboard_item/dashboard_item";
import { PieChart } from "../pie_chart/pie_chart";
import { DashboardFollowedLeagues } from "./DashboardFollowedLeagues/DashboardFollowedLeagues";

class DashboardSportsGames extends Component {
    static template = "sports_betting.DashboardSports";
    static components = { Layout, DashboardItemSports, PieChart, DashboardFollowedLeagues };

    setup() {
        this.hasData = false;
        this.display = {
            controlPanel: {},
        };
        this.chartData = {};
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.action = useService("action");
        console.log(this.statistics)
    }

    openCountries(){
        this.action.doAction("sports_betting.action_sports_country");
    }

    openLeagues(){
        this.action.doAction("sports_betting.action_sports_league");
    }

    openTeams(){
        this.action.doAction("sports_betting.action_sports_team");
    }

    openConfiguration() {
        console.log("openConfiguration");
    }
}

registry.category("lazy_components").add("DashboardSports", DashboardSportsGames);