from odoo import models, fields  # type: ignore


class SportsLeague(models.Model):
    _name = "sports.league"
    _description = "Sports League"

    name = fields.Char(string="League Name", required=True)
    country_id = fields.Many2one(
        "sports.country", string="Country", required=True, ondelete='restrict'
    )
    session_id = fields.Many2one(
        "sports.session", string="Season", required=True, ondelete='restrict'
    )
    logo = fields.Char(string="League Logo")
    league_id_api = fields.Integer(string="API League ID", required=True)
    follow = fields.Boolean(string="Follow", default=False)
    team_ids = fields.One2many("sports.team", "league_id", string="Teams")

    _sql_constraints = [
        (
            'unique_league_per_season',
            'unique(league_id_api, session_id)',
            'This league already exists for the selected season.'
        )
    ]

    def sync_leagues_data(self):
        data = {
            'league': self.league_id_api,
            'season': self.session_id.name
        }
        model = self.env['sports.api.import']
        model.fetch_teams_from_api(**data)
