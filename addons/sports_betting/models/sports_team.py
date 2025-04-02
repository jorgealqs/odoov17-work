from odoo import api, models, fields  # type: ignore


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
    standings_id = fields.One2many(
        "sports.standings", "team_id", string="Standings"
    )
    rank = fields.Integer(
        string="Rank",
        compute="_compute_standings_data",
        store=True
    )
    points = fields.Integer(
        string="Points",
        compute="_compute_standings_data",
        store=True,
    )
    goals_diff = fields.Integer(
        string="Goals Difference",
        compute="_compute_standings_data",
        store=True
    )
    played = fields.Integer(
        string="Played",
        compute="_compute_standings_data",
        store=True
    )
    wins = fields.Integer(
        string="Wins",
        compute="_compute_standings_data",
        store=True
    )
    draws = fields.Integer(
        string="Draws",
        compute="_compute_standings_data",
        store=True
    )
    loses = fields.Integer(
        string="Losses",
        compute="_compute_standings_data",
        store=True
    )
    goals_for = fields.Integer(
        string="Goals For",
        compute="_compute_standings_data",
        store=True
    )
    goals_against = fields.Integer(
        string="Goals Against",
        compute="_compute_standings_data",
        store=True
    )

    @api.depends(
        "standings_id.points",
        "standings_id.rank",
        "standings_id.goals_diff",
        "standings_id.stats_ids",
        "standings_id.update_date"
    )
    def _compute_standings_data(self):
        """Compute both rank and points from latest standings data."""
        for team in self:
            latest_standing = team.standings_id.filtered(
                lambda s: s.team_id == team
            ).sorted(key=lambda r: r.update_date, reverse=True)[:1]
            # Obtener el más reciente

            if latest_standing:
                team.points = latest_standing.points
                team.rank = latest_standing.rank
                team.goals_diff = latest_standing.goals_diff
                data = latest_standing.stats_ids.filtered(
                    lambda s: s.type == "overall"
                )
                team.played = data.played
                team.wins = data.win
                team.draws = data.draw
                team.loses = data.lose
                team.goals_for = data.goals_for
                team.goals_against = data.goals_against
            else:
                team.points = 0
                team.rank = 0
                team.goals_diff = 0
                team.played = 0
                team.wins = 0
                team.goals_for = 0
                team.goals_against = 0

    _sql_constraints = [
        (
            'unique_team_per_season',
            'unique(name, league_id, session_id)',
            'This team already exists in the selected league and season.'
        )
    ]
