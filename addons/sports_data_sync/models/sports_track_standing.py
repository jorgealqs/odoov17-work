import logging
from odoo import models, fields  # type: ignore

_logger = logging.getLogger(__name__)


class SportsTrackStanding(models.Model):
    _name = 'sports.track.standing'
    _description = 'League Standing'

    team_id = fields.Many2one(
        'sports.track.team',
        required=True,
        ondelete='cascade'
    )
    country_id = fields.Many2one(
        'sports.track.country',
        required=True
    )
    league_id = fields.Many2one(
        'sports.track.league',
        required=True
    )
    session_id = fields.Many2one(
        'sports.track.session',
        required=True
    )
    group = fields.Char()
    rank = fields.Integer()
    points = fields.Integer()
    goals_diff = fields.Integer()
    form = fields.Char()
    status = fields.Char()
    description = fields.Char()
    update_date = fields.Datetime()

    # Datos globales
    played = fields.Integer()
    win = fields.Integer()
    draw = fields.Integer()
    lose = fields.Integer()
    goals_for = fields.Integer()
    goals_against = fields.Integer()

    # Local
    home_played = fields.Integer()
    home_win = fields.Integer()
    home_draw = fields.Integer()
    home_lose = fields.Integer()
    home_goals_for = fields.Integer()
    home_goals_against = fields.Integer()

    # Visitante
    away_played = fields.Integer()
    away_win = fields.Integer()
    away_draw = fields.Integer()
    away_lose = fields.Integer()
    away_goals_for = fields.Integer()
    away_goals_against = fields.Integer()

    def _save_or_update_standing(self, *args, **kwargs):
        vals = {
            'team_id': kwargs.get('team_id'),
            'country_id': kwargs.get('country_id'),
            'league_id': kwargs.get('league_id'),
            'session_id': kwargs.get('session_id'),

            # Datos del ranking
            'rank': kwargs.get('vals_rank', {}).get('rank'),
            'points': kwargs.get('vals_rank', {}).get('points'),
            'goals_diff': kwargs.get('vals_rank', {}).get('goalsDiff'),
            'group': kwargs.get('vals_rank', {}).get('group'),
            'form': kwargs.get('vals_rank', {}).get('form'),
            'status': kwargs.get('vals_rank', {}).get('status'),
            'description': kwargs.get('vals_rank', {}).get('description'),
            'update_date': kwargs.get('vals_rank', {}).get('update'),

            # Datos globales
            'played': kwargs.get('all_stading', {}).get('played'),
            'win': kwargs.get('all_stading', {}).get('win'),
            'draw': kwargs.get('all_stading', {}).get('draw'),
            'lose': kwargs.get('all_stading', {}).get('lose'),
            'goals_for': kwargs.get('all_stading', {}).get('goals_for'),
            'goals_against': kwargs.get(
                'all_stading', {}
            ).get('goals_against'),

            # Local
            'home_played': kwargs.get('home', {}).get('played'),
            'home_win': kwargs.get('home', {}).get('win'),
            'home_draw': kwargs.get('home', {}).get('draw'),
            'home_lose': kwargs.get('home', {}).get('lose'),
            'home_goals_for': kwargs.get('home', {}).get('goals_for'),
            'home_goals_against': kwargs.get('home', {}).get('goals_against'),

            # Visitante
            'away_played': kwargs.get('away', {}).get('played'),
            'away_win': kwargs.get('away', {}).get('win'),
            'away_draw': kwargs.get('away', {}).get('draw'),
            'away_lose': kwargs.get('away', {}).get('lose'),
            'away_goals_for': kwargs.get('away', {}).get('goals_for'),
            'away_goals_against': kwargs.get('away', {}).get('goals_against'),
        }

        validate = self.search([
            ('team_id', '=', kwargs.get('team_id')),
            ('country_id', '=', kwargs.get('country_id')),
            ('league_id', '=', kwargs.get('league_id')),
            ('session_id', '=', kwargs.get('session_id')),
            ('group', '=', kwargs.get('vals_rank').get('group')),
        ], limit=1)
        if validate:
            validate.write(vals)
        else:
            self.create(vals)
