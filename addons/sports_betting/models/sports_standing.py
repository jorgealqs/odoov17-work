from odoo import models, fields  # type: ignore


class SportsStandings(models.Model):
    _name = 'sports.standings'
    _description = 'Sports Standings'

    rank = fields.Integer(string='Rank')
    team_id = fields.Many2one(
        'sports.team', string='Team', required=True
    )
    points = fields.Integer(string='Points')
    goals_diff = fields.Integer(string='Goals Difference')
    group = fields.Char(string='Group')
    form = fields.Char(string='Form')
    status = fields.Selection([
        ('same', 'Same'),
        ('up', 'Up'),
        ('down', 'Down')
    ], string='Status')
    description = fields.Char(string='Description')
    update_date = fields.Datetime(string='Last Update')
    # Relación con estadísticas
    stats_ids = fields.One2many(
        'sports.standings.stats',
        'standings_id',
        string='Statistics'
    )
