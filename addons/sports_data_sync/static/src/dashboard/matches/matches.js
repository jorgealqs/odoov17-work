/** @odoo-module */

import { Component } from "@odoo/owl"

export class MatchesSportsSyncData extends Component {
    static template = "sports_sync_data.Games"
    static props = {
        data: {
            type: Object,
        },
        onClickFetchFixture:{
            type: Function,
        }
    }

    onClickFetchFixture(ev) {
        const id = parseInt(ev.currentTarget.dataset.id, 10);
        const round = this.props.data.find(r => r.id === id);

        if (!round) {
            console.error("No se encontró el round con id:", id);
            return;
        }

        const filter = {
            leagueId: round.league_id[0],
            sessionId: round.session_id[0],
            homeTeamId: round.home_team_id[0],
            awayTeamId: round.away_team_id[0],
        }
        this.props.onClickFetchFixture(filter);
    }


}