from odoo import models, api
import requests
from bs4 import BeautifulSoup
import logging
from .lottery_constants import URLS, HEADERS, BALOTO  # 👈 importas las URLs
import re
from datetime import datetime

_logger = logging.getLogger(__name__)


class LotteryImporterBaloto(models.AbstractModel):
    _name = 'lottery.importer.baloto'
    _description = 'Importador de resultados Baloto'

    @api.model
    def run_import(self, game):
        game_id = game.id
        url = game.website
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            # levanta un error si status_code no es 200
            soup = BeautifulSoup(response.content, 'html.parser')
            container = soup.find('div', id='container-banner-results')
            if container:
                h2_tag = container.find('h2')
                h3_tag = container.find('h3')
                if h2_tag and h3_tag:
                    draw_text = h2_tag.get_text(strip=True)
                    date_text = h3_tag.get_text(strip=True)
                    match = re.search(r'#(\d+)', draw_text)
                    draw_number = int(match.group(1)) if match else None
                    _logger.info(
                        f"✅ Sorteo: {draw_number} | Fecha: {date_text}"
                    )
                    url_result = f"{URLS['revancha']}/{draw_number}"
                    if game.name == BALOTO:
                        url_result = f"{URLS['baloto']}/{draw_number}"
                    self._get_data(
                        url_result, game_id, game.name, date_text, draw_number
                    )
                else:
                    _logger.warning(
                        "No se encontraron los tags h2 o h3 dentro del "
                        "container"
                    )
            else:
                _logger.warning(
                    "No se encontró el contenedor con "
                    "id='container-banner-results'"
                )

        except requests.exceptions.HTTPError as http_err:
            _logger.error(f"❌ Error HTTP al acceder a {url}: {http_err}")
            return
        except requests.exceptions.RequestException as req_err:
            _logger.error(f"❌ Error de conexión al acceder a {url}: {req_err}")
            return

    def _get_data(self, url, game_id, game_name, date_text, draw_number):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            _logger.error(f"❌ Error al obtener datos de {url}: {e}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        # Encuentra todas las bolas amarillas
        yellow_balls = soup.find_all('div', class_='yellow-ball')
        yellow_numbers = [ball.get_text(strip=True) for ball in yellow_balls]

        # Encuentra la bola roja
        red_ball = soup.find('div', class_='red-ball')
        red_number = red_ball.get_text(strip=True) if red_ball else None
        yellow_numbers.append(red_number)

        if yellow_numbers and red_number:
            _logger.info(
                f"\n\n\n🎱 Números Baloto: {yellow_numbers} + Rojo: "
                f"{red_number} \n\n\n"
            )
            # Aquí podrías guardar en la DB si quieres
        else:
            _logger.warning(
                "⚠️ No se encontraron los números del resultado correctamente."
            )
        # Extraer acumulado
        acumulado_tag = soup.find(
            'div', class_='text-center my-3 gotham-medium dark-blue fs-6'
        )
        if acumulado_tag:
            texto = acumulado_tag.get_text(strip=True)
            match = re.search(r'\$\s*([\d\.]+)', texto)
            acumulado = match.group(1) if match else None
            _logger.info(f"💰 Acumulado del sorteo: {acumulado} millones")
        else:
            _logger.warning("⚠️ No se encontró el acumulado del sorteo.")

        winner_main_prize = self._get_winner_main_prize(soup)
        _logger.warning(f"\n\n {winner_main_prize} \n\n")
        draw_date = self._parse_draw_date(date_text)
        draw = self.env['lottery.draw'].create({
            'name': f"{game_name} {date_text}",
            'draw_date': draw_date,
            'game_id': game_id,
            'jackpot': acumulado or 0.0,
            "draw_number": int(draw_number),
            "win": winner_main_prize
        })
        # 🎯 Guardar números amarillos
        for i, num in enumerate(yellow_numbers):
            color = 1 if i == len(yellow_numbers) - 1 else 3
            self.env['lottery.draw.number'].create({
                'draw_id': draw.id,
                'number': int(num),
                'color': int(color),
            })

    def _parse_draw_date(self, texto_fecha):
        meses = {
            'Enero': 'January',
            'Febrero': 'February',
            'Marzo': 'March',
            'Abril': 'April',
            'Mayo': 'May',
            'Junio': 'June',
            'Julio': 'July',
            'Agosto': 'August',
            'Septiembre': 'September',
            'Octubre': 'October',
            'Noviembre': 'November',
            'Diciembre': 'December'
        }
        partes = texto_fecha.split(' ', 1)[1]
        for es, en in meses.items():
            if es in partes:
                partes = partes.replace(es, en)
                break
        return datetime.strptime(partes, "%d de %B de %Y").date()

    def _get_winner_main_prize(self, soup):
        tabla = soup.find(
            'table', class_='table table-striped gotham-medium text-center'
        )
        if not tabla:
            _logger.warning("⚠️ No se encontró la tabla de premios.")
            return None

        primer_tr = tabla.find('tr')  # Primer fila de la tabla
        if not primer_tr:
            _logger.warning("⚠️ No se encontró el primer <tr> en la tabla.")
            return None

        celdas = primer_tr.find_all('td')
        if len(celdas) < 4:
            _logger.warning("⚠️ No hay suficientes <td> en la primera fila.")
            return None

        cantidad_ganadores = celdas[2].get_text(strip=True)
        _logger.info(f"🎲 Ganadores del premio mayor: {cantidad_ganadores}")

        if cantidad_ganadores == '0':
            return False  # No cayó el premio mayor
        else:
            return True   # Sí cayó
