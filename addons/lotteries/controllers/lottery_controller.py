# -*- coding: utf-8 -*-

from odoo import http
import logging
from ..models.lottery_constants import (
    BALOTO_SEARCH,
    SEARCH_MILOTO,
    SEARCH_BALOTO_REVANCHA,
    SEARCH_COLORLOTO,
    SEARCH_MEDELLIN
)

from .services.dashboard import (
    get_lottery_data,
    get_last_raws,
    get_forecast_filter,
    get_forecast_result_filters,
    get_crypto_data
)

_logger = logging.getLogger(__name__)


class LotteryController(http.Controller):

    @http.route('/lottery/statistics', type='json', auth='user')
    def get_lottery_statistics(self, **kw):
        """Returns statistics for all lottery types"""
        try:
            return {
                "baloto": get_lottery_data(BALOTO_SEARCH),
                "revancha": get_lottery_data(SEARCH_BALOTO_REVANCHA),
                "miloto": get_lottery_data(SEARCH_MILOTO),
                "colorloto": get_lottery_data(SEARCH_COLORLOTO),
                "medellin": get_lottery_data(SEARCH_MEDELLIN),
                "last_draws": get_last_raws(),
                "crypto": get_crypto_data()
            }
        except Exception as e:
            _logger.error(f"Error getting lottery statistics: {str(e)}")
            return {'error': 'Failed to fetch lottery statistics'}

    @http.route('/lottery/forecast', type='json', auth='user')
    def get_forecast_data(self, **kw):
        """Returns forecast data for all lottery types"""
        try:
            return get_forecast_filter()
        except Exception as e:
            _logger.error(f"Error getting forecast data: {str(e)}")
            return {'error': 'Failed to fetch forecast data'}
        return get_forecast_filter()

    @http.route('/lottery/forecast/results', type='json', auth='user')
    def get_forecast_results(self, **kw):
        try:
            return get_forecast_result_filters(**kw)
        except Exception as e:
            _logger.error(f"Error getting forecast data: {str(e)}")
            return {'error': 'Failed to fetch forecast data'}
