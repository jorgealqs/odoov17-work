# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import logging
from ..models.lottery_constants import (
    BALOTO_SEARCH,
    SEARCH_MILOTO,
    SEARCH_BALOTO_REVANCHA,
    SEARCH_COLORLOTO
)

_logger = logging.getLogger(__name__)


class LotteryController(http.Controller):

    @http.route('/lottery/statistics', type='json', auth='user')
    def get_lottery_statistics(self, **kw):
        """Returns statistics for all lottery types"""
        try:
            return {
                'baloto': self._get_lottery_data(BALOTO_SEARCH),
                'revancha': self._get_lottery_data(SEARCH_BALOTO_REVANCHA),
                'miloto': self._get_lottery_data(SEARCH_MILOTO),
                'colorloto': self._get_lottery_data(SEARCH_COLORLOTO),
            }
        except Exception as e:
            _logger.error(f"Error getting lottery statistics: {str(e)}")
            return {'error': 'Failed to fetch lottery statistics'}

    def _get_lottery_data(self, search_terms):
        """Generic function to return statistics for a given lottery type"""
        games = request.env['lottery.game'].search([
            ('name', 'in', search_terms)
        ], limit=10)

        if not games:
            _logger.warning(f"No games found for: {search_terms}")
            return {'total': 0, 'win': 0, 'fall': 0}

        draws = request.env['lottery.draw'].search([
            ('game_id', 'in', games.ids)
        ])

        total = len(draws)
        wins = len(draws.filtered(lambda d: d.win))
        falls = total - wins

        return {
            'total': total,
            'win': wins,
            'fall': falls,
        }
