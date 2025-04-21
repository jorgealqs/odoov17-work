from odoo.http import request
import logging

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
