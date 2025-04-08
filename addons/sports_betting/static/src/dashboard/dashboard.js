/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "../dashboard_item/dashboard_item";
import { PieChart } from "../pie_chart/pie_chart";

class DashboardGames extends Component {
    static template = "sports_betting.Dashboard";
    static components = { Layout, DashboardItem, PieChart};

    setup() {
        this.display = {
            controlPanel: {},
        };
        this.isLoaded = false; // <--- Estado para indicar si los datos están listos
        this.chartData = {};
        this.statistics = useService("awesome_dashboard.statistics");
        this.action = useService("action");
        onWillStart(async () => {
            this.statistics = await this.statistics.loadStatistics();
            const stats = this.statistics.countries;
            const stats_leagues_data = this.statistics.leagues;
            this.chartData = {
                "In session": stats.with_sessions.count,
                "Without session": stats.without_sessions.count,
            };
            const stats_leagues = this.statistics.leagues;
            this.chartDataLeague = {
                "Following": stats_leagues.followed.count,
                "Not Following": stats_leagues.not_followed.count,
            };
            this.isLoaded = true; // <--- Marca que los datos ya están listos
            this.inSessionCountries = stats.with_sessions.names.map((c) => c.name).join(', ');
            this.inSessionLeagues = stats_leagues_data.followed.names.map((c) => c.name).join(', ');
        });
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
}

registry.category("lazy_components").add("DashboardGames", DashboardGames);