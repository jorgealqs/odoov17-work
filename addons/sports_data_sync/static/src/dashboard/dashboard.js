/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from  "@odoo/owl";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { PieChart } from "../pie_chart/pie_chart";
import { LeagueCards } from "./league_cards/league_cards";
import { MatchesSportsSyncData } from "./matches/matches";


class DashboardSportsSyncData extends Component {
    static template = "sports_data_sync.DashboardSync";
    static components = { Layout, PieChart, LeagueCards, MatchesSportsSyncData };
    static props = {}

    setup() {
        this.action = useService("action");
        this.display = {
            controlPanel: {},
        };
        this.statistics = useState(useService("sports_sync_data.statistics"));
    }

    openCountries(){
        this.action.doAction("sports_data_sync.action_sports_track_country");
    }

    openLeagues(){
        this.action.doAction("sports_data_sync.action_sports_track_league");
    }

    openTeams(){
        this.action.doAction("sports_data_sync.action_sports_track_team");
    }

    openStandings(){
        this.action.doAction("sports_data_sync.action_sports_track_standing");
    }

    openFixtures(){
        this.action.doAction("sports_data_sync.action_sports_track_fixture");
    }

    onClickLeague(league) {
        const { league_id_table, country_id, session_id, league_name } = league;

        // Por ejemplo, si querés usar esos valores en un action:
        this.action.doAction({
            type: "ir.actions.act_window",
            name: `Tabla de posiciones de ${league_name}`,
            res_model: "sports.track.standing",
            views: [
                [false, "list"],
            ],
            domain: [
                ["country_id", "=", country_id],
                ["league_id", "=", league_id_table],
                ["session_id", "=", session_id],
            ],
            context: {
                group_by: "group",
            },
        });
    }

    onClickFetchFixture(filter) {
        const { leagueId, homeTeamId, awayTeamId, sessionId } = filter;
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Standings",
            res_model: "sports.track.standing",
            views: [
                [false, "list"],
            ],
            domain: [
                ["session_id.id", "=", sessionId],
                ["league_id.id", "=", leagueId],
                "|",  // Esto significa "o" en los filtros de Odoo
                ["team_id.id", "=", homeTeamId],
                ["team_id.id", "=", awayTeamId],
            ],
            context: {
                group_by: "group",
            },
        });
    }
}

// remember the tag name we put in the first step
registry.category("lazy_components").add("DashboardSportsSync", DashboardSportsSyncData);