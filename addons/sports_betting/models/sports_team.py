from odoo import models, fields  # type: ignore


class SportsTeam(models.Model):
    _name = "sports.team"
    _description = "Sports Team"

    name = fields.Char(string="Team Name", required=True)
    team_id_api = fields.Integer(string="API Team ID", required=True)
    code = fields.Char(string="Team Code")
    founded = fields.Integer(string="Founded Year")
    national = fields.Boolean(string="Is National Team?", default=False)
    logo = fields.Char(string="Team Logo")  # URL de la imagen del equipo

    venue_id = fields.Many2one(
        "sports.venue", string="Venue"
    )
    league_id = fields.Many2one(
        "sports.league", string="League", required=True
    )
    session_id = fields.Many2one(
        "sports.session", string="Season", required=True
    )
    country_id = fields.Many2one(
        "sports.country",
        string="Country",
        related="league_id.country_id",
        store=True
    )

    _sql_constraints = [
        (
            'unique_team_per_season',
            'unique(name, league_id, session_id)',
            'This team already exists in the selected league and season.'
        )
    ]
