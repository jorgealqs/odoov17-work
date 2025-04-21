/** @odoo-module **/

import { Component } from  "@odoo/owl";


export class LeagueCards extends Component {
    static template = "sports_data_sync.DashboardLeagueCards";
    static props = {
        leagues: Array,
        onClickLeague: Function,
    }

    onClickLeague(ev) {
        const leagueId = ev.currentTarget.dataset.leagueId;
        const league = this.props.leagues.find(l => l.league_id == leagueId);
        this.props.onClickLeague(league);
    }
}