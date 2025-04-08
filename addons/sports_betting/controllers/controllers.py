# -*- coding: utf-8 -*-

import logging

from odoo import http  # type: ignore
from odoo.http import request  # type: ignore

logger = logging.getLogger(__name__)


class AwesomeDashboard(http.Controller):
    @http.route('/awesome_dashboard/statistics', type='json', auth='user')
    def get_statistics(self):
        countries = request.env['sports.country'].sudo().search([])
        leagues = request.env['sports.league'].sudo().search([])

        countries_with_sessions = []
        countries_without_sessions = []

        for country in countries:
            if country.session_id:
                countries_with_sessions.append(
                    {'name': country.name, 'id': country.id}
                )
            else:
                countries_without_sessions.append(country.name)

        leagues_followed = []
        leagues_not_followed = []

        for league in leagues:
            league_data = {'name': league.name, 'id': league.id}
            if league.follow:
                leagues_followed.append(league_data)
            else:
                leagues_not_followed.append(league_data)

        return {
            'countries': {
                'with_sessions': {
                    'count': len(countries_with_sessions),
                    'names': countries_with_sessions,
                },
                'without_sessions': {
                    'count': len(countries_without_sessions),
                    'names': countries_without_sessions,
                }
            },
            'leagues': {
                'followed': {
                    'count': len(leagues_followed),
                    'names': leagues_followed,
                },
                'not_followed': {
                    'count': len(leagues_not_followed),
                    'names': leagues_not_followed,
                }
            }
        }
