from odoo import models, fields, api  # type: ignore
import logging

_logger = logging.getLogger(__name__)


class SportsTrackBet(models.Model):
    _name = 'sports.track.bet'
    _description = 'Sports Track Bet'
    _order = "name"

    name = fields.Char(string='Bet Description', required=True)
    bookmaker_id = fields.Many2one(
        'sports.track.bookmaker',
        string='Bookmaker',
        help='Select the betting house'
    )
    stake = fields.Float(string='Total Stake (Amount Bet)', required=True)
    result = fields.Selection([
        ('pending', 'Pending'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ], string='Overall Result', default='pending')
    payout = fields.Float(
        string='Total Payout',
        compute='_compute_payout', store=True
    )

    prediction_ids = fields.One2many(
        'sports.track.bet.prediction',
        'bet_id',
        string='Predictions'
    )
    bettor_id = fields.Many2one(
        'res.users',  # Usuario que hace la apuesta
        string='Bettor',
        default=lambda self: self.env.user,
        help="User who placed the bet"
    )

    @api.depends(
        'result',
        'stake',
        'prediction_ids.odds',
        'prediction_ids.result'
    )
    def _compute_payout(self):
        for bet in self:
            total = 1.0
            won_all = True
            for pred in bet.prediction_ids:
                if pred.result != 'won':
                    won_all = False
                    break
                total *= pred.odds or 1.0
            bet.payout = bet.stake * total if won_all else 0.0
