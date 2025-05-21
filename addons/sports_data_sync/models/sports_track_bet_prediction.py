from odoo import models, fields  # type: ignore
import logging

_logger = logging.getLogger(__name__)


class SportsTrackBetPrediction(models.Model):
    _name = 'sports.track.bet.prediction'
    _description = 'Bet Prediction'

    bet_id = fields.Many2one(
        'sports.track.bet',
        string='Bet',
        required=True,
        ondelete='cascade'
    )
    fixture_id = fields.Many2one(
        'sports.track.fixture',
        string='Fixture',
        required=True
    )
    odds = fields.Float(string='Odds')
    date = fields.Date(string="Prediction Date", default=fields.Date.today)
    bet_type_ids = fields.Many2many(
        'sports.track.bet.type',
        'sports_bet_prediction_type_rel',
        'prediction_id',
        'bet_type_id',
        string='Bet Types'
    )
    result = fields.Selection([
        ('pending', 'Pending'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ], string='Result', default='pending')
