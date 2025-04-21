import logging
from odoo import models, fields, exceptions  # type: ignore
from .api_football_connector import APIFootballConnector

_logger = logging.getLogger(__name__)


class SportsTrackLeague(models.Model):
    _name = 'sports.track.league'
    _description = 'Sports Track League'
    _order = "name desc"

    # Model fields
    name = fields.Char(string='Name', required=True)
    id_league = fields.Integer(string='League ID', required=True)
    type_league = fields.Char(string='Type')
    logo = fields.Char(string='Logo URL')
    start = fields.Date(string='Start Date')
    end = fields.Date(string='End Date')
    follow = fields.Boolean(string='Follow', default=False)
    # Related fields
    country_id = fields.Many2one(
        'sports.track.country',
        string='Country',
        required=True,
        ondelete='restrict'
    )
    session_id = fields.Many2one(
        'sports.track.session',
        string='Session',
        required=True,
        ondelete='restrict'
    )

    def _sync_leagues(self, *args, **kwargs):
        connector = APIFootballConnector()
        country = kwargs.get('country')
        session = kwargs.get('session')

        leagues = connector.get_leagues(
            country_name=country.get('name'),
            country_code=country.get('country_code'),
            season=session.get('year')
        )
        data = {
            'country_id': country.get('id'),
            'session_id': session.get('id'),
            'leagues': leagues
        }
        self._save_or_update_leagues(**data)

    def _save_or_update_leagues(self, *args, **kwargs):
        leagues = kwargs.get('leagues')
        country_id = kwargs.get('country_id')
        session_id = kwargs.get('session_id')

        for league in leagues:
            league_data = league.get('league', {})
            season_data = league.get('seasons', [{}])[0]

            vals = {
                'name': league_data.get('name'),
                'id_league': league_data.get('id'),
                'type_league': league_data.get('type'),
                'logo': league_data.get('logo'),
                'start': season_data.get('start'),
                'end': season_data.get('end'),
                'country_id': country_id,
                'session_id': session_id,
            }

            existing = self.search([
                ('id_league', '=', vals['id_league']),
                ('country_id', '=', country_id),
                ('session_id', '=', session_id),
            ], limit=1)

            if existing:
                existing.write(vals)
                _logger.info(
                    f"[UPDATED] League {vals['name']} (ID {vals['id_league']})"
                )
            else:
                self.create(vals)
                _logger.info(
                    f"[CREATED] League {vals['name']} (ID {vals['id_league']})"
                )

    def sync_standings(self):
        for league in self:
            if not league.follow:
                raise exceptions.UserError(
                    "No session found for this league."
                )
            data = {
                'league': {
                    'id': league.id,
                    'name': league.name,
                    'id_league': league.id_league,
                },
                'session': {
                    'id': league.session_id.id,
                    'year': league.session_id.year,
                },
                'country': {
                    'id': league.country_id.id,
                    'name': league.country_id.name,
                }
            }
            self.env['sports.track.team']._sync_teams(**data)
