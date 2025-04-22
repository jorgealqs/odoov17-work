import logging
from odoo.http import request
from datetime import datetime, timedelta
import pytz

_logger = logging.getLogger(__name__)


def get_country_stats():
    Country = request.env['sports.track.country']

    # Países con al menos una sesión
    countries_with_sessions = Country.search([
        ('session_id', '!=', False)
    ])
    # Países sin sesiones
    countries_without_sessions = Country.search([
        ('session_id', '=', False)
    ])

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

    countries_with_sessions = Country.search([
        ('session_id', '!=', False)
    ])

    followed_leagues = []

    for country in countries_with_sessions:
        session = country.session_id
        leagues = League.search([
            ('follow', '=', True),
            ('country_id', '=', country.id),
            ('session_id', '=', session.id)
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


def get_rounds_leagues():
    colombia_tz = pytz.timezone('America/Bogota')
    leagues = get_followed_leagues()
    all_fixtures = []

    today = datetime.now(colombia_tz)
    next_days = today + timedelta(days=2)

    _logger.info(f"\n\n{today} {next_days} \n\n")

    for league in leagues:
        # 🚀 Traemos todos los standings UNA SOLA VEZ por liga+sesión
        standings = request.env['sports.track.standing'].search_read(
            [
                ('league_id', '=', league['league_id_table']),
                ('session_id', '=', league['session_id']),
            ],
            fields=['team_id', 'rank', 'points']
        )
        # 📌 Convertimos a dict para acceder más rápido
        standings_dict = {
            s['team_id'][0]: {'rank': s['rank'], 'points': s['points']}
            for s in standings
        }

        # 🔁 Traemos fixtures normalmente
        fixtures = request.env['sports.track.fixture'].search_read(
            [
                ('country_id', '=', league['country_id']),
                ('session_id', '=', league['session_id']),
                ('league_id', '=', league['league_id_table']),
                ('match_date', '>=', today),
                ('match_date', '<=', next_days),
            ],
            fields=[],  # todos los campos
        )

        # 🎯 Añadimos rank/points desde standings_dict sin más consultas
        for fixture in fixtures:
            home_id = fixture['home_team_id'][0]
            away_id = fixture['away_team_id'][0]

            fixture['home_team_rank'] = standings_dict.get(
                home_id, {}
            ).get('rank')
            fixture['home_team_points'] = standings_dict.get(
                home_id, {}
            ).get('points')
            fixture['away_team_rank'] = standings_dict.get(
                away_id, {}
            ).get('rank')
            fixture['away_team_points'] = standings_dict.get(
                away_id, {}
            ).get('points')

            all_fixtures.append(fixture)

    return sorted(all_fixtures, key=lambda x: x['match_date'])
