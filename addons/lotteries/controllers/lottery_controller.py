# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
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
                'last_draws': self._get_last_raws()
            }
        except Exception as e:
            _logger.error(f"Error getting lottery statistics: {str(e)}")
            return {'error': 'Failed to fetch lottery statistics'}

    def _get_last_raws(self, limit_per_game=1):
        """Returns the last draw for each lottery game type"""
        result = {}
        games = request.env['lottery.game'].search([])

        for game in games:
            draw = request.env['lottery.draw'].search(
                [('game_id', '=', game.id)],
                limit=limit_per_game,
                order='draw_date desc'
            )
            if draw:
                result[game.name] = {
                    'id': draw.id,
                    'draw_date': draw.draw_date.isoformat(),
                    'numbers': [n.number for n in draw.number_ids],
                }

        return result

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

    @http.route('/lottery/forecast', type='json', auth='user')
    def get_forecast_data(self, **kw):
        """Returns forecast data for all lottery types"""
        games = request.env['lottery.game'].search([])
        result = [
            {
                'value': game.id,
                'name': game.name,
            }
            for game in games
        ]
        return {
            'games': result,
            'options': self._get_forecast_options(),
        }

    def _get_forecast_options(self):
        """Returns forecast options for all lottery types"""
        return [
            {'value': 'frequency', 'name': 'Frecuencia de Números'},
            {'value': 'repeats', 'name': 'Combinaciones Repetidas'},
            {'value': 'hot_numbers', 'name': 'Números Más Frecuentes'},
        ]

    @http.route('/lottery/forecast/results', type='json', auth='user')
    def get_forecast_results(self, **kw):
        args = kw.get('args')
        if args and isinstance(args, list) and isinstance(args[0], dict):
            data = args[0]
            game_id = data.get('game_id')
            option_id = data.get('option_id')
        else:
            game_id = option_id = None

        if not game_id or not option_id:
            return {'error': 'Missing game or option ID'}

        draws = request.env['lottery.draw'].search([
            ('game_id', '=', int(game_id))
        ], order='draw_date asc')  # orden por fecha para análisis temporal

        if not draws:
            return {'error': 'No draws found'}

        # Construir DataFrame desde los datos de Odoo
        data = []
        for draw in draws:
            for num in draw.number_ids:
                data.append({
                    'date': draw.draw_date,
                    'number': num.number,
                    'color': num.color
                })

        if option_id == 'frequency':
            return self._get_number_frequency(data)
        elif option_id == 'repeats':
            return self._get_number_repeats(data)

        return {'error': 'Invalid option'}

    def _get_number_repeats(self, data):
        _logger.info(f"\n\n_get_number_repeats: {data}\n\n")

    def _get_number_frequency(self, data):
        if not data:
            return {'error': 'No data received'}

        df = pd.DataFrame(data)
        if df.empty or 'number' not in df or 'date' not in df:
            return {'error': 'Invalid data format'}

        # Asegurar que las fechas están en formato datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])  # eliminar fechas inválidas

        # Calcular frecuencia
        freq = df['number'].value_counts().reset_index()
        freq.columns = ['number', 'frequency']

        # Calcular días promedio entre apariciones
        avg_intervals = []
        for number in df['number'].unique():
            dates = df[df['number'] == number]['date'].sort_values()
            if len(dates) < 2:
                avg_days = None
            else:
                days_between = dates.diff().dropna().dt.days
                avg_days = round(
                    days_between.mean(), 2) if not days_between.empty else None

            all_dates = dates.dt.date.astype(str).tolist()

            avg_intervals.append({
                'number': number,
                'avg_days_between': avg_days,
                'last_seen': dates.max().date().isoformat(),
                'all_dates': all_dates
            })

        df_intervals = pd.DataFrame(avg_intervals)

        # Unir con frecuencia
        result_df = pd.merge(
            freq, df_intervals, on='number'
        ).sort_values(by='frequency', ascending=False)
        result_df = result_df.replace({np.nan: None})

        return {'results': result_df.to_dict(orient='records')}
