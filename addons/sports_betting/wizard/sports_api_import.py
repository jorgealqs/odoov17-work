import logging
from typing import Dict, Any, Optional  # type: ignore
from odoo import _, models, exceptions  # type: ignore
from ..models.api_utils import APIFootballHelper
from datetime import datetime

_logger = logging.getLogger(__name__)


class SportsAPIImport(models.TransientModel):
    _name = 'sports.api.import'
    _description = 'Import Data from API Football'

    def _create_country(self, name: str, code: str, flag: str) -> None:
        """Create a country if it doesn't exist.

        Args:
            name: Country name
            code: Country code
            flag: URL to country flag
        """
        country_model = self.env['sports.country']
        if not code:
            _logger.warning(
                "Country '%s' has no code, assigning default", name
            )
            return

        if not country_model.search([('code', '=', code)], limit=1):
            country_model.create({
                'name': name,
                'code': code,
                'flag': flag
            })
            _logger.info("Created country: %s (%s)", name, code)
        else:
            _logger.debug("Country already exists: %s (%s)", name, code)

    def fetch_countries_from_api(self):
        """Llama a la API y crea los países en Odoo, incluyendo 'World'"""
        _logger.info("Iniciando la importación de países desde la API.")

        # Obtener datos de la API usando la clase reutilizable
        data = APIFootballHelper.fetch_api_data('/countries')

        if "response" in data:
            for country in data["response"]:
                self._create_country(
                    country["name"],
                    country["code"],
                    country["flag"]
                )

        _logger.info("Importación de países finalizada correctamente.")
        return {'type': 'ir.actions.act_window_close'}

    def _get_leagues_to_fetch(
        self,
        season: Optional[str] = None,
        code: Optional[str] = None
    ) -> models.Model:
        """Get leagues that should be fetched based on criteria.

        Args:
            season: Optional season filter
            code: Optional country code filter

        Returns:
            Record set of leagues to fetch

        Raises:
            exceptions.UserError: If no leagues are found
        """
        domain = []
        if season and code:
            domain = [('code', '=', code), ('session_id.name', '=', season)]
        else:
            domain = [('session_id', '!=', False)]

        leagues = self.env['sports.country'].search(domain)
        if not leagues:
            raise exceptions.UserError(
                _("No countries with active sessions found to fetch leagues.")
            )
        return leagues

    def _prepare_league_values(
        self,
        league_data: Dict[str, Any],
        country_id: int, session_id: int
    ) -> Dict[str, Any]:
        """Prepare values for league creation/update.

        Args:
            league_data: Raw league data from API
            country_id: ID of related country
            session_id: ID of related session

        Returns:
            Dictionary with prepared values
        """
        return {
            "league_id_api": league_data["id"],
            "name": league_data["name"],
            "logo": league_data["logo"],
            "country_id": country_id,
            "session_id": session_id,
        }

    def _create_or_update_league(
        self,
        league_vals: Dict[str, Any],
        session_id: int
    ) -> None:
        """Create or update a league record.

        Args:
            league_vals: Prepared league values
            session_id: ID of related session
        """
        league_model = self.env['sports.league']
        existing_league = league_model.search([
            ('league_id_api', '=', league_vals["league_id_api"]),
            ('session_id', '=', session_id)
        ], limit=1)

        if existing_league:
            existing_league.write(league_vals)
            _logger.info(
                "Updated League: %s (%s)",
                league_vals["name"],
                league_vals["league_id_api"]
            )
        else:
            league_model.create(league_vals)
            _logger.info(
                "Created New League: %s (%s)",
                league_vals["name"],
                league_vals["league_id_api"]
            )

    def fetch_leagues_from_api(self, **kwargs) -> Dict[str, Any]:
        """
            Fetch leagues data from API Football for countries with active
            sessions.
        """
        try:
            leagues = self._get_leagues_to_fetch(
                kwargs.get('season'),
                kwargs.get('code')
            )

            for country in leagues:
                data = APIFootballHelper.fetch_api_data('/leagues', params={
                    'code': country.code,
                    'season': country.session_id.name,
                    'current': 'true'
                })

                if "response" in data:
                    for response in data["response"]:
                        league_vals = self._prepare_league_values(
                            response["league"],
                            country.id,
                            country.session_id.id
                        )
                        self._create_or_update_league(
                            league_vals, country.session_id.id
                        )

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Leagues Imported Successfully!"),
                    'message': _(
                        "The leagues have been successfully fetched and "
                        "updated."
                    ),
                    'sticky': False,
                    'type': 'success',
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }

        except Exception as e:
            _logger.error("Error fetching leagues: %s", str(e))
            raise exceptions.UserError(
                _("Failed to fetch leagues: %s") % str(e)
            )

    def _create_fetch_teams_from_api(self, *args, **kwargs):
        if kwargs:
            league_id = kwargs.get('league')
            season = kwargs.get('season')
            leagues_followed = self.env[
                'sports.league'
            ].search(
                [
                    ('league_id_api', '=', league_id),
                    ('session_id.name', '=', season)
                ]
            )
            _logger.info(
                f"\n\n league: {league_id} season: {season} \n\n"
            )
        else:
            leagues_followed = self.env[
                'sports.league'
            ].search([('follow', '=', True)])

        if not leagues_followed:
            raise exceptions.UserError(
                _("No followed leagues found to import teams.")
            )

        for league in leagues_followed:
            params = {
                'league': league.league_id_api,
                'season': league.session_id.name
            }
            data = APIFootballHelper.fetch_api_data('/teams', params=params)

            if "response" in data:
                for response in data["response"]:
                    team_data = response["team"]
                    venue_data = response.get("venue", {})
                    venue_vals = {
                        "name": venue_data.get("name") or "Unnamed Venue",
                        "address": venue_data.get("address") or "No Address",
                        "city": venue_data.get("city") or "Unknown City",
                        "capacity": venue_data.get("capacity") or 0,
                        "surface":
                        venue_data.get("surface") or "Unknown Surface",
                        "image": venue_data.get("image") or "",
                    }

                    # Buscar si el equipo ya existe en la liga y sesión
                    existing_team = self.env['sports.team'].search([
                        ('team_id_api', '=', team_data["id"]),
                        ('league_id', '=', league.id),
                        ('session_id', '=', league.session_id.id)
                    ], limit=1)

                    if existing_team:
                        existing_team.write({
                            "name": team_data.get("name"),
                            "code": team_data.get("code"),
                            "founded": team_data.get("founded"),
                            "national": team_data.get("national"),
                            "logo": team_data.get("logo"),
                            "venue_id": existing_team.venue_id
                        })
                        _logger.info(
                            f"Updated team: {team_data.get('name')} "
                            f"(ID: {team_data.get('id')})"
                        )
                    else:
                        # Si el equipo no existe, lo creamos
                        venue_id = self.env[
                            'sports.team.venue'
                        ].create(venue_vals).id
                        team_vals = {
                            "name": team_data.get("name"),
                            "team_id_api": team_data.get("id"),
                            "code": team_data.get("code"),
                            "founded": team_data.get("founded"),
                            "national": team_data.get("national"),
                            "logo": team_data.get("logo"),
                            "league_id": league.id,
                            "session_id": league.session_id.id,
                            "venue_id": venue_id
                        }
                        self.env['sports.team'].create(team_vals)
                        _logger.info(
                            f"Created new team: {team_data.get('name')} "
                            f"(ID: {team_data.get('id')})"
                        )

    def _prepare_standings_values(
        self,
        team_data: Dict[str, Any],
        team_record: models.Model
    ) -> Dict[str, Any]:
        """Prepare values for standings creation/update.

        Args:
            team_data: Raw team data from API
            team_record: Team record in Odoo

        Returns:
            Dictionary with prepared values
        """
        update_date_str = team_data.get("update")
        update_date = datetime.strptime(
            update_date_str[:19], "%Y-%m-%dT%H:%M:%S"
        ) if update_date_str else False

        # Usar .get() para proporcionar valores por defecto
        # si las claves no existen
        return {
            "rank": team_data.get("rank", 0),
            "team_id": team_record.id,
            "points": team_data.get("points", 0),
            "goals_diff": team_data.get("goalsDiff", 0),
            "group": team_data.get("group", ""),
            "form": team_data.get("form", ""),
            "status": team_data.get("status", ""),
            "description": team_data.get("description", ""),
            "update_date": update_date,
        }

    def _create_or_update_standings(
        self,
        standings_vals: Dict[str, Any],
        team_data: Dict[str, Any]
    ) -> models.Model:
        """Create or update standings record.

        Args:
            standings_vals: Prepared standings values
            team_data: Raw team data from API

        Returns:
            Created or updated standings record
        """
        standings_model = self.env['sports.standings']
        existing_standing = standings_model.search([
            ('team_id', '=', standings_vals['team_id']),
            ('update_date', '=', standings_vals['update_date']),
            ('group', '=', standings_vals['group'])
        ], limit=1)

        if existing_standing:
            existing_standing.write(standings_vals)
            _logger.info("Updated standings for %s", team_data['name'])
            return existing_standing
        else:
            new_standing = standings_model.create(standings_vals)
            _logger.info("Created new standings for %s", team_data['name'])
            return new_standing

    def _create_fetch_standings_from_api(self, *args, **kwargs):
        if kwargs:
            league_id = kwargs.get('league')
            season = kwargs.get('season')
            leagues_followed = self.env['sports.league'].search([
                ('league_id_api', '=', league_id),
                ('session_id.name', '=', season)
            ])
            _logger.info(f"\n\n league: {league_id} season: {season} \n\n")
        else:
            leagues_followed = self.env['sports.league'].search(
                [('follow', '=', True)]
            )

        if not leagues_followed:
            raise exceptions.UserError(
                _("No followed leagues found to import standings.")
            )

        for league in leagues_followed:
            params = {
                'league': league.league_id_api,
                'season': league.session_id.name
            }
            data = APIFootballHelper.fetch_api_data(
                '/standings', params=params
            )

            if "response" in data:
                for response in data["response"]:
                    standings_data = response["league"]["standings"]

                    for standing in standings_data:
                        for team in standing:
                            # Agregar log para depuración
                            _logger.debug(
                                "Team data received from API: %s", team
                            )

                            team_data = team.get("team", {})
                            team_stats_overall = team.get("all", {})
                            team_stats_home = team.get("home", {})
                            team_stats_away = team.get("away", {})

                            # Combinar datos del equipo con estadísticas
                            team_data.update({
                                "rank": team.get("rank", 0),
                                "points": team.get("points", 0),
                                "goalsDiff": team.get("goalsDiff", 0),
                                "form": team.get("form", ""),
                                "status": team.get("status", ""),
                                "group": team.get("group", ""),
                                "description": team.get("description", ""),
                            })

                            team_record = self.env['sports.team'].search([
                                ('team_id_api', '=', team_data.get("id")),
                                ('league_id', '=', league.id),
                                ('session_id', '=', league.session_id.id)
                            ], limit=1)

                            if not team_record:
                                _logger.warning(
                                    "Team %s not found in Odoo. Skipping...",
                                    team_data.get('name', 'Unknown')
                                )
                                continue

                            standings_vals = self._prepare_standings_values(
                                team_data,
                                team_record
                            )

                            # Buscar si existe un standing para este equipo
                            # en la misma fecha
                            existing_standing = self.env[
                                'sports.standings'
                            ].search([
                                ('team_id', '=', team_record.id),
                                (
                                    'update_date',
                                    '=',
                                    standings_vals['update_date']
                                ),
                                ('group', '=', team_data.get('group'))
                            ], limit=1)

                            if existing_standing:
                                # Actualizar el standing existente
                                existing_standing.write(standings_vals)
                                standings_record = existing_standing
                                _logger.info(
                                    f"Updated standings for "
                                    f"{team_data['name']}"
                                )
                            else:
                                # Crear nuevo standing
                                standings_record = (
                                    self._create_or_update_standings(
                                        standings_vals, team_data
                                    )
                                )

                            stats_vals = [
                                {
                                    "standings_id": standings_record.id,
                                    "type": stat_type,
                                    "played": stat_data["played"],
                                    "win": stat_data["win"],
                                    "draw": stat_data["draw"],
                                    "lose": stat_data["lose"],
                                    "goals_for": stat_data["goals"]["for"],
                                    "goals_against": stat_data[
                                        "goals"
                                    ]["against"],
                                } for stat_type, stat_data in [
                                    ("overall", team_stats_overall),
                                    ("home", team_stats_home),
                                    ("away", team_stats_away)
                                ]
                            ]

                            # Actualizar o crear estadísticas
                            for stat_val in stats_vals:
                                existing_stat = self.env[
                                    'sports.standings.stats'
                                ].search([
                                    ('standings_id', '=', standings_record.id),
                                    ('type', '=', stat_val['type'])
                                ], limit=1)

                                if existing_stat:
                                    existing_stat.write(stat_val)
                                    _logger.info(
                                        f"Updated {stat_val['type']} "
                                        f"stats for {team_data['name']}"
                                    )
                                else:
                                    self.env[
                                        'sports.standings.stats'
                                    ].create(stat_val)
                                    _logger.info(
                                        f"Created {stat_val['type']} stats "
                                        f"for {team_data['name']}"
                                    )

    def fetch_teams_from_api(self, *args, **kwargs):
        """Fetch teams data from API Football for each followed league."""
        _logger.info("\n\nStarting teams import from API\n\n")
        self._create_fetch_teams_from_api(**kwargs)
        self._create_fetch_standings_from_api(**kwargs)
        _logger.info("Teams import finished")
