from odoo import models, fields, api  # type: ignore
import logging

_logger = logging.getLogger(__name__)


class SportsTrackBet(models.Model):
    _name = 'sports.track.bet'
    _inherit = ['mail.thread']
    _description = 'Sports Track Bet'
    _order = "reference desc"

    reference = fields.Char(
        string='Reference',
        default='New'
    )
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
        'res.users',
        string='Bettor',
        default=lambda self: self.env.user,
        help="User who placed the bet"
    )

    def create(self, vals):
        if vals.get('reference', 'New') == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'sports.track.bet'
            )
        return super().create(vals)

    @api.depends(
        'stake',
        'prediction_ids.odds',
        'prediction_ids.result'
    )
    def _compute_payout(self):
        for bet in self:
            total_odds = 1.0
            for pred in bet.prediction_ids:
                total_odds *= pred.odds or 1.0

            # Este es el posible pago sin importar resultado
            bet.payout = bet.stake * total_odds if bet.prediction_ids else 0.00

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"[{rec.reference}] {rec.bookmaker_id.name}"

    def action_won(self):
        for rec in self:
            rec.result = 'won'

    def action_lost(self):
        for rec in self:
            rec.result = 'lost'
            rec.payout = 0.00

    def sync_bets(self):
        pending_bets = self.search([('result', '=', 'pending')])

        for bet in pending_bets:
            all_won = True
            total_odds = 1.0

            for pred in bet.prediction_ids:
                if pred.result != 'pending':
                    continue

                fixture = self.env['sports.track.fixture'].search([
                    ('fixture_api_id', '=', pred.fixture_id.fixture_api_id)
                ], limit=1)

                if not fixture:
                    _logger.warning(
                        f"❌ Fixture {pred.fixture_id.fixture_api_id} no found."
                    )
                    all_won = False  # por si falta un resultado
                    continue

                if fixture.home_goals > fixture.away_goals:
                    comparation = "1"
                elif fixture.home_goals < fixture.away_goals:
                    comparation = "2"
                else:
                    comparation = "X"

                if comparation.upper() in str(pred.bet_type_id.name).upper():
                    pred.result = 'won'
                    total_odds *= pred.odds or 1.0
                else:
                    pred.result = 'lost'
                    all_won = False
            _logger.info(all_won)

            # Actualizar estado general de la apuesta
            # if all_won:
            #     bet.result = 'won'
            # else:
            #     bet.result = 'lost'
            #     bet.payout = 0.0
