from odoo import models, fields  # type: ignore


class SportsStandingsStats(models.Model):
    _name = 'sports.standings.stats'
    _description = 'Standings Statistics'

    standings_id = fields.Many2one(
        'sports.standings',
        string='Standings',
        required=True,
        ondelete='cascade'
    )
    type = fields.Selection([
        ('overall', 'Overall'),
        ('home', 'Home'),
        ('away', 'Away')
    ], string="Stats Type", required=True)

    played = fields.Integer(string='Played')
    win = fields.Integer(string='Wins')
    draw = fields.Integer(string='Draws')
    lose = fields.Integer(string='Losses')
    goals_for = fields.Integer(string='Goals For')
    goals_against = fields.Integer(string='Goals Against')
