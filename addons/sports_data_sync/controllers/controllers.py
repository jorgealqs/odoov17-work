# -*- coding: utf-8 -*-

import logging
from odoo import http
from .services.dashboard import (
    get_country_stats,
    get_followed_leagues
)

_logger = logging.getLogger(__name__)


class SportsDataController(http.Controller):
    @http.route('/sports_data/dashboard', type='json', auth='user')
    def get_sports_data(self, **kw):
        try:
            follow_countries = get_country_stats()
            follow_leagues = get_followed_leagues()
            return {
                'follow_countries': follow_countries,
                'follow_leagues': follow_leagues,
            }

        except Exception as e:
            _logger.error(f"Error fetching sports data: {str(e)}")
            return {
                'status': 'error',
                'message': 'Failed to fetch sports data',
            }
