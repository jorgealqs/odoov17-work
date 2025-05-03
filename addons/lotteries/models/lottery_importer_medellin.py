from odoo import models, api
import requests
import logging
from bs4 import BeautifulSoup

_logger = logging.getLogger(__name__)


class LotteryImporterMedellin(models.AbstractModel):
    _name = 'lottery.importer.medellin'
    _description = 'Importador de resultados Lotería de Medellín'

    NUM = {"4781"}

    @api.model
    def run_import(self, game):
        try:
            for num in self.NUM:
                data = self._extract_data(game, int(num))
                self._save_data(data, game)
        except requests.exceptions.HTTPError as http_err:
            _logger.error(f"❌ Error HTTP al acceder a {http_err}")
            return
        except requests.exceptions.RequestException as req_err:
            _logger.error(f"❌ Error de conexión al acceder a {req_err}")
            return

    def _save_data(self, data, game):
        """
        Guarda los datos del sorteo en la base de datos.
        """
        draw = self.env['lottery.draw'].create({
            'name': f"{game.name} {data['draw_date']}",
            'draw_date': data['draw_date'],
            'game_id': game.id,
            'jackpot': float("16.00"),
            "draw_number": int(data['draw_number'])
        })
        # Crear los dígitos del número ganador
        if data['number']:
            for digit in data['number']:
                self.env['lottery.draw.number'].create({
                    'draw_id': draw.id,
                    'number': int(digit)
                })

    def _extract_data(self, game, num):
        """
        Extrae los datos del sorteo desde la Lotería de Medellín vía POST AJAX.
        """

        url = "https://loteriademedellin.com.co/wp-admin/admin-ajax.php"

        payload = {
            "action": "wp_get_results_lottery_template",
            "is_front": "true",
            "lottery_id": "16",
            "draw_id": num,
            "post_type": "results_template",
        }

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://loteriademedellin.com.co",
            "Referer":
            "https://loteriademedellin.com.co/historico-de-resultados/",
        }

        try:
            response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()
            json_data = response.json()
        except Exception as e:
            _logger.error(f"Error al hacer la solicitud: {e}")
            return {}

        html = json_data.get("html", "")
        _logger.info(html)
        selected = json_data.get("selected", {})

        # Parsear el HTML con BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        numbers = soup.select(".elementor-lottery-jackpot-number")

        # Devolver los datos estructurados
        return {
            "number": numbers[0].text.strip() if len(numbers) > 0 else None,
            "serie": numbers[1].text.strip() if len(numbers) > 1 else None,
            "draw_date": selected.get("meta_value"),
            "draw_number": num,
        }
