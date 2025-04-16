# -*- coding: utf-8 -*-

import pandas as pd
from babel.dates import format_date
import numpy as np
from odoo import http
from odoo.http import request
import logging
from ..models.lottery_constants import (
    BALOTO_SEARCH,
    SEARCH_MILOTO,
    SEARCH_BALOTO_REVANCHA,
    SEARCH_COLORLOTO,
    SEARCH_MEDELLIN
)
from itertools import combinations
from collections import defaultdict

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
                'medellin': self._get_lottery_data(SEARCH_MEDELLIN),
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
                # Formatear fecha en español
                draw_date_str = format_date(
                    draw.draw_date, format='long', locale='es_ES'
                )
                result[game.name] = {
                    'id': draw.id,
                    'draw_date': draw_date_str,
                    'name': game.name,
                    'numbers': [{
                        'number': n.number,
                        'color': n.color
                    } for n in draw.number_ids],
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
        ]

    @http.route('/lottery/forecast/results', type='json', auth='user')
    def get_forecast_results(self, **kw):
        args = kw.get('args')
        if args and isinstance(args, list) and isinstance(args[0], dict):
            data = args[0]
            game_id = data.get('game_id')
            option_id = data.get('option_id')
            combination = data.get('number')
        else:
            game_id = option_id = combination = None

        if not game_id or not option_id:
            return {'error': 'Missing game or option ID'}

        draws = request.env['lottery.draw'].search([
            ('game_id', '=', int(game_id))
        ], order='draw_date asc')  # orden por fecha para análisis temporal

        if not draws:
            return {'error': 'No draws found'}
        data_frecuency = self._data_frecuency(draws)

        if option_id == 'frequency':
            return self._get_number_frequency(data_frecuency)
        elif option_id == 'repeats':
            combination = int(combination) if str(combination).isdigit() else 2
            return self._get_all_combinations_frequency(
                draws, int(combination)
            )

        return {'error': 'Invalid option'}

    def _data_frecuency(self, draws):
        data = []
        for draw in draws:
            for num in draw.number_ids:
                data.append({
                    'date': draw.draw_date,
                    'number': num.number,
                    'color': num.color
                })
        return data

    def _get_all_combinations_frequency(self, draws, n=2):
        if not draws or not isinstance(n, int) or n < 2:
            return {'error': 'Invalid draw data or combination length'}

        combo_data = defaultdict(list)

        for draw in draws:
            date = draw.draw_date
            numbers = [num.number for num in draw.number_ids]
            if len(numbers) >= n:
                for combo in combinations(numbers, n):
                    combo_key = "-".join(map(str, combo))
                    combo_data[combo_key].append(date)

        results = []
        for combo_str, dates in combo_data.items():
            dates = sorted(pd.to_datetime(dates))
            frequency = len(dates)

            if frequency >= 2:
                days_between = pd.Series(dates).diff().dropna().dt.days
                avg_days = round(
                    days_between.mean(), 2
                ) if not days_between.empty else None
            else:
                avg_days = None

            results.append({
                'number': combo_str,
                'frequency': frequency,
                'avg_days_between': avg_days,
                'last_seen': dates[-1].date().isoformat(),
                'all_dates': [d.date().isoformat() for d in dates]
            })

        # Ordenar por frecuencia descendente
        results = sorted(
            results,
            key=lambda x: (x['frequency'], x['last_seen']),
            reverse=True
        )

        return {'results': results}

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
