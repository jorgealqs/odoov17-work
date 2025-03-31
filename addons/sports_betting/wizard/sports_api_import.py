import logging
from odoo import _, models, exceptions  # type: ignore
from ..models.api_utils import APIFootballHelper

_logger = logging.getLogger(__name__)


class SportsAPIImport(models.TransientModel):
    _name = 'sports.api.import'
    _description = 'Import Data from API Football'

    def _create_country(self, name, code, flag):
        """Crea un país solo si no existe previamente"""
        country_model = self.env['sports.country']

        # Asegurar que el código no sea NULL
        if not code:
            _logger.warning(
                "El país '%s' no tiene código, asignando uno por defecto.",
                name
            )
            # Ejemplo: "World" → "WORLD"

        existing_country = country_model.search([('code', '=', code)], limit=1)
        if not existing_country:
            country_model.create({
                'name': name,
                'code': code,
                'flag': flag
            })
            _logger.info("País creado: %s (%s)", name, code)
        else:
            _logger.info("País ya existente: %s (%s)", name, code)

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

    def fetch_leagues_from_api(self):
        """
        Fetch leagues data from API Football only for countries with active
        sessions.
        If the league already exists, update it; otherwise, create a new one.
        """
        _logger.info("Starting leagues import from API")

        # Obtener los países que tienen al menos una sesión activa
        league_follow = self.env['sports.country'].search(
            [('session_id', '!=', False)]
        )

        if not league_follow:
            raise exceptions.UserError(
                _(
                    "At least one country must have an active session to fetch"
                    " leagues."
                )
            )

        for country in league_follow:
            params = {
                'code': country.code,
                'season': country.session_id.name,
                'current': 'true'
            }
            data = APIFootballHelper.fetch_api_data('/leagues', params=params)

            if "response" in data:
                for response in data["response"]:
                    league = response["league"]

                    league_vals = {
                        "league_id_api": league["id"],
                        "name": league["name"],
                        "logo": league["logo"],
                        "country_id": country.id,
                        "session_id": country.session_id.id,
                    }

                    # Verificar si la liga ya existe
                    existing_league = self.env['sports.league'].search([
                        ('league_id_api', '=', league["id"]),
                        ('session_id', '=', country.session_id.id)
                    ], limit=1)

                    if existing_league:
                        # Si la liga ya existe, actualizar los datos
                        existing_league.write(league_vals)
                        _logger.info(
                            "Updated League: %s (%s)", league["name"],
                            league["id"]
                        )
                    else:
                        # Si no existe, crear la nueva liga
                        self.env['sports.league'].create(league_vals)
                        _logger.info(
                            "Created New League: %s (%s)",
                            league["name"], league["id"]
                        )

        _logger.info("Leagues import finished")
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Leagues Imported Successfully!"),
                'message': _(
                    "The leagues have been successfully fetched and updated."
                ),
                'sticky': False,
                # False para que desaparezca después de unos segundos
                'type': 'success',
                # Tipo de mensaje (success, warning, danger, info)
                'next': {'type': 'ir.actions.act_window_close'},
                # Cierra la ventana
            }
        }

    def fetch_teams_from_api(self):
        """Fetch teams data from API Football for each followed league."""
        _logger.info("\n\nStarting teams import from API\n\n")

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

        _logger.info("Teams import finished")
