import logging
from odoo import models, fields  # type: ignore
from .api_football_connector import APIFootballConnector
from datetime import datetime

_logger = logging.getLogger(__name__)


class SportsTrackFixture(models.Model):
    _name = 'sports.track.fixture'
    _description = 'Football Track Fixtures'
    _rec_name = 'fixture_api_id'
    _rec_names_search = [
        'fixture_api_id', 'home_team_id.name', 'away_team_id.name'
    ]

    country_id = fields.Many2one(
        'sports.track.country',
        required=True
    )
    session_id = fields.Many2one(
        'sports.track.session',
        required=True
    )
    league_id = fields.Many2one(
        'sports.track.league',
        string="League",
        ondelete='cascade',
        required=True
    )

    # Fixture info
    fixture_api_id = fields.Char(
        string="API Fixture ID",
        required=True, index=True
    )
    referee = fields.Char(string="Referee")
    timezone = fields.Char(string="Timezone")
    match_date = fields.Datetime(string="Match Date", required=True)
    match_timestamp = fields.Integer(string="Timestamp")

    # Teams
    home_team_id = fields.Many2one(
        'sports.track.team', string="Home Team", required=True
    )
    away_team_id = fields.Many2one(
        'sports.track.team', string="Away Team", required=True
    )

    # Goals
    home_goals = fields.Integer(string="Goals Home")
    away_goals = fields.Integer(string="Goals Away")

    # Scores
    halftime_home = fields.Integer(string="Halftime Home")
    halftime_away = fields.Integer(string="Halftime Away")
    fulltime_home = fields.Integer(string="Fulltime Home")
    fulltime_away = fields.Integer(string="Fulltime Away")
    extratime_home = fields.Integer(string="Extratime Home")
    extratime_away = fields.Integer(string="Extratime Away")
    penalty_home = fields.Integer(string="Penalty Home")
    penalty_away = fields.Integer(string="Penalty Away")

    def _sync_fixtures(self, *args, **kwargs):
        connector = APIFootballConnector()

        country = kwargs.get('country')
        session = kwargs.get('session')
        league = kwargs.get('league')

        fixtures = connector.get_fixtures(
            league.get('id_league'),
            session.get('year')
        )

        for fixture in fixtures:
            fixture_data = fixture.get('fixture', {})
            teams_data = fixture.get('teams', {})
            goals_data = fixture.get('goals', {})
            score_data = fixture.get('score', {})

            raw_date = fixture_data.get('date')
            try:
                match_date = self._parse_api_date(raw_date)
            except ValueError:
                match_date = False

            home_team_id = self._get_team_id(
                team_id=teams_data.get('home', {}).get('id'),
                league_id=league.get('id'),
                session_id=session.get('id')
            )

            away_team_id = self._get_team_id(
                team_id=teams_data.get('away', {}).get('id'),
                league_id=league.get('id'),
                session_id=session.get('id')
            )

            # Si alguno no existe, no creamos el fixture
            if not home_team_id or not away_team_id:
                _logger.warning(
                    f"Fixture omitido: home_team_id={home_team_id}, "
                    f"away_team_id={away_team_id}"
                )
                continue

            vals_fixture = {
                "country_id": country.get('id') or False,
                "session_id": session.get('id') or False,
                "league_id": league.get('id') or False,
                "fixture_api_id": fixture_data.get('id') or False,
                "referee": fixture_data.get('referee') or False,
                "timezone": fixture_data.get('timezone') or False,
                "match_date": match_date,
                "match_timestamp": fixture_data.get('timestamp') or False,
                "home_team_id": home_team_id,
                "away_team_id": away_team_id,
                "home_goals": goals_data.get(
                    'home'
                ) if goals_data.get('home') is not None else False,
                "away_goals": goals_data.get(
                    'away'
                ) if goals_data.get('away') is not None else False,
                "halftime_home": score_data.get(
                    'halftime', {}
                ).get('home') or False,
                "halftime_away": score_data.get(
                    'halftime', {}
                ).get('away') or False,
                "fulltime_home": score_data.get(
                    'fulltime', {}
                ).get('home') or False,
                "fulltime_away": score_data.get(
                    'fulltime', {}
                ).get('away') or False,
                "extratime_home": score_data.get(
                    'extratime', {}
                ).get('home') or False,
                "extratime_away": score_data.get(
                    'extratime', {}
                ).get('away') or False,
                "penalty_home": score_data.get(
                    'penalty', {}
                ).get('home') or False,
                "penalty_away": score_data.get(
                    'penalty', {}
                ).get('away') or False,
            }

            existing = self.search([
                ('fixture_api_id', '=', fixture_data.get('id')),
                ('league_id', '=', league.get('id')),
                ('session_id', '=', session.get('id'))
            ], limit=1)

            if existing:
                _logger.info(f"\nUpdate Synced Fixture: {vals_fixture}\n")
                existing.write(vals_fixture)
            else:
                _logger.info("\nCreate Synced Fixture:\n")
                self.create(vals_fixture)

    def _get_team_id(self, team_id=None, league_id=None, session_id=None):
        team = self.env['sports.track.team'].search([
            ('api_id', '=', team_id),
            ('league_id', '=', league_id),
            ('session_id', '=', session_id),
        ], limit=1)
        return team.id if team else False

    def _parse_api_date(self, api_date):
        """
        Parse the fixture date from the API format.
        """
        try:
            return datetime.strptime(api_date[:-6], '%Y-%m-%dT%H:%M:%S')
        except ValueError as e:
            _logger.error(f"Error parsing date: {e}")
            return None

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"[{rec.fixture_api_id}] {rec.home_team_id.name} vs "
                f"{rec.away_team_id.name} [{rec.country_id.country_code}]"
            )
