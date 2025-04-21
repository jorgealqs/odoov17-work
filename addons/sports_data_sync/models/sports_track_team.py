import logging
from collections import defaultdict
from datetime import datetime
from odoo import models, fields  # type: ignore
from .api_football_connector import APIFootballConnector

_logger = logging.getLogger(__name__)


class SportsTrackTeam(models.Model):
    _name = 'sports.track.team'
    _description = 'Football Track Team'

    name = fields.Char(required=True)
    logo = fields.Char()
    api_id = fields.Integer(string="API ID", required=True, index=True)
    country_id = fields.Many2one('sports.track.country')
    league_id = fields.Many2one('sports.track.league')
    session_id = fields.Many2one('sports.track.session')

    def _sync_teams(self, *args, **kwargs):
        connector = APIFootballConnector()
        league = kwargs.get('league')
        session = kwargs.get('session')
        country = kwargs.get('country')

        result = connector.get_standings(
            league.get('id_league'), session.get('year')
        )

        data = {
            'league_id': league.get('id'),
            'session_id': session.get('id'),
            'country_id': country.get('id'),
            'result': result
        }
        self._save_or_update_teams(**data)

    def _save_or_update_teams(self, *args, **kwargs):
        try:
            result = kwargs.get('result')
            if not result or not isinstance(
                result, list
            ) or not result[0].get('league'):
                _logger.warning(
                    "Respuesta vacía o malformada al obtener standings."
                )
                return

            standings = result[0]['league'].get('standings', [])

            for teams in standings:
                for team in teams:
                    if team.get('form') is None:
                        continue

                    iso_date = team.get('update')
                    try:
                        update_date = datetime.fromisoformat(
                            iso_date.replace('Z', '+00:00')
                        )
                        update_str = update_date.strftime('%Y-%m-%d %H:%M:%S')
                    except Exception as e:
                        _logger.error(
                            f"Error al convertir la fecha: {iso_date} -> {e}"
                        )
                        update_str = None

                    vals_rank = {
                        "rank": team.get('rank'),
                        "points": team.get('points'),
                        "goalsDiff": team.get('goalsDiff'),
                        "group": team.get('group'),
                        "form": team.get('form'),
                        "status": team.get('status'),
                        "description": team.get('description'),
                        "update": update_str,
                    }

                    team_vals = self._prepare_team_data(team.get('team'))
                    all_stading = self._prepare_standing_data(team.get('all'))
                    home = self._prepare_standing_data(team.get('home'))
                    away = self._prepare_standing_data(team.get('away'))

                    vals_team = {
                        'name': team_vals.get('name'),
                        'logo': team_vals.get('logo'),
                        'api_id': team_vals.get('api_id'),
                        'country_id': kwargs.get('country_id'),
                        'league_id': kwargs.get('league_id'),
                        'session_id': kwargs.get('session_id'),
                    }

                    vals_standing = {
                        'league_id': kwargs.get('league_id'),
                        'session_id': kwargs.get('session_id'),
                        'country_id': kwargs.get('country_id'),
                        'vals_rank': vals_rank,
                        'all_stading': all_stading,
                        'home': home,
                        'away': away,
                    }

                    validate = self.search([
                        ('api_id', '=', team_vals.get('api_id')),
                        ('country_id', '=', kwargs.get('country_id')),
                        ('league_id', '=', kwargs.get('league_id')),
                        ('session_id', '=', kwargs.get('session_id')),
                    ], limit=1)

                    if validate:
                        _logger.info(f"Update equipo: {team_vals.get('name')}")
                        validate.write(vals_team)
                        team_id = validate
                    else:
                        team_id = self.create(vals_team)
                        _logger.info(f"Create equipo: {team_vals.get('name')}")

                    vals_standing['team_id'] = team_id.id
                    self.env[
                        'sports.track.standing'
                    ]._save_or_update_standing(**vals_standing)

        except Exception as e:
            _logger.error(f"Error al guardar o actualizar equipos: {e}")

    def _prepare_team_data(self, team_data):
        return {
            'name': team_data.get('name'),
            'logo': team_data.get('logo'),
            'api_id': team_data.get('id'),
        }

    def _prepare_standing_data(self, standing_data):
        data = defaultdict(lambda: 0, standing_data or {})
        goals = data.get('goals') or {}
        return {
            "played": data['played'],
            "win": data['win'],
            "draw": data['draw'],
            "lose": data['lose'],
            "goals_for": goals.get('for', 0),
            "goals_against": goals.get('against', 0),
        }
