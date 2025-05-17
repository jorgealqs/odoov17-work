import logging
from odoo.http import request  # type: ignore
from datetime import datetime
import pytz  # type: ignore

_logger = logging.getLogger(__name__)


def get_country_stats():
    Country = request.env['sports.track.country']

    countries_with_sessions = Country.search([('session_id', '!=', False)])
    countries_without_sessions = Country.search([('session_id', '=', False)])

    return {
        'with_sessions': {
            'count': len(countries_with_sessions),
            'names': [
                f"{c.name} - {c.session_id.year}" if c.session_id else c.name
                for c in countries_with_sessions
            ],
        },
        'without_sessions': {
            'count': len(countries_without_sessions),
            'names': countries_without_sessions.mapped('name'),
        }
    }


def get_followed_leagues():
    Country = request.env['sports.track.country']
    League = request.env['sports.track.league']

    followed_leagues = []

    for country in Country.search([('session_id', '!=', False)]):
        session = country.session_id
        leagues = League.search([
            ('follow', '=', True),
            ('country_id', '=', country.id),
            ('session_id', '=', session.id),
        ])
        for league in leagues:
            followed_leagues.append({
                'league_name': league.name,
                'league_id': league.id_league,
                'country': country.name,
                'session': session.year,
                'logo': league.logo,
                'country_id': country.id,
                'session_id': session.id,
                'league_id_table': league.id,
            })

    return followed_leagues


def get_rounds_leagues(only_ids=False):

    tz = pytz.timezone('America/Bogota')
    today = datetime.now(tz)
    tomorrow = today.replace(hour=23, minute=59, second=59, microsecond=59)

    all_fixtures = []

    for league in get_followed_leagues():
        standings_dict = get_standings_dict(
            league_id=league['league_id_table'],
            session_id=league['session_id']
        )

        fixtures = get_upcoming_fixtures(
            country_id=league['country_id'],
            league_id=league['league_id_table'],
            session_id=league['session_id'],
            start_date=today,
            end_date=tomorrow
        )

        for fixture in fixtures:
            home_id = fixture['home_team_id'][0]
            away_id = fixture['away_team_id'][0]

            fixture.update({
                'home_team_rank': standings_dict.get(
                    home_id, {}
                ).get('rank'),
                'home_team_points': standings_dict.get(
                    home_id, {}).get('points'),
                'away_team_rank': standings_dict.get(away_id, {}).get('rank'),
                'away_team_points': standings_dict.get(
                    away_id, {}).get('points'),
                'home_last_matches': get_last_matches(
                    home_id, league['session_id'],
                    league['league_id_table'], fixture['match_date'], 'home'),
                'away_last_matches': get_last_matches(
                    away_id, league['session_id'],
                    league['league_id_table'], fixture['match_date'], 'away'),
                'prediction': get_prediction(fixture['id'])
            })

            all_fixtures.append(fixture)
    if only_ids:
        return [
            {
                'id': fixture['id'],
                'fixture_api_id': fixture['fixture_api_id']
            } for fixture in sorted(
                all_fixtures, key=lambda x: x['match_date'])
        ]

    return sorted(all_fixtures, key=lambda x: x['match_date'])


def get_prediction(id_prediction):
    Prediction = request.env['sports.track.predictions']
    prediction = Prediction.search_read([
        ("fixture_id", "=", id_prediction)
    ], limit=1)
    return prediction[0] if prediction else None


def get_standings_dict(league_id, session_id):
    standings = request.env['sports.track.standing'].search_read(
        [('league_id', '=', league_id), ('session_id', '=', session_id)],
        fields=['team_id', 'rank', 'points']
    )
    return {
        s['team_id'][0]: {'rank': s['rank'], 'points': s['points']}
        for s in standings
    }


def get_upcoming_fixtures(
        country_id, league_id, session_id, start_date, end_date
):
    return request.env['sports.track.fixture'].search_read(
        [
            ('country_id', '=', country_id),
            ('league_id', '=', league_id),
            ('session_id', '=', session_id),
            ('match_date', '>=', start_date),
            ('match_date', '<=', end_date),
        ],
        fields=[]
    )


def get_last_matches(team_id, session_id, league_id, date, game, limit=5):
    Fixture = request.env['sports.track.fixture']

    domain = [
        ('session_id', '=', session_id),
        ('match_date', '<', date),
        '|',
        ('home_team_id.id', '=', team_id),
        ('away_team_id.id', '=', team_id),
    ]
    if league_id:
        domain.append(('league_id', '=', league_id))

    matches = Fixture.search_read(
        domain,
        fields=[
            'match_date', 'home_team_id', 'away_team_id',
            'home_goals', 'away_goals'],
        order='match_date desc',
        limit=limit
    )

    result = []
    for match in matches:
        is_home = match['home_team_id'][0] == team_id
        opponent = match[
            'away_team_id'
        ][1] if is_home else match['home_team_id'][1]
        goals_for = match['home_goals'] if is_home else match['away_goals']
        goals_against = match['away_goals'] if is_home else match['home_goals']

        outcome = 'Win' if (
            goals_for > goals_against
        ) else 'Loss' if goals_for < goals_against else 'Draw'

        result.append({
            'date': match['match_date'],
            'opponent': opponent,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'result': outcome,
            'game': game,
        })

    return result
