from odoo import models, api
import requests
from bs4 import BeautifulSoup
import logging
from .lottery_constants import HEADERS, URLS  # 👈 importas las URLs
import re
from datetime import datetime

_logger = logging.getLogger(__name__)


class LotteryImporterMiloto(models.AbstractModel):
    _name = 'lottery.importer.miloto'
    _description = 'Importador de resultados Miloto'

    @api.model
    def run_import(self, game):
        url = game.website
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            # 🔍 Buscar el div que contiene fecha y sorteo
            container = soup.find('div', class_='container-how-play')
            if not container:
                _logger.warning(
                    "⚠️ No se encontró el contenedor "
                    "con la clase 'container-how-play'"
                )
                return
            date_text = container.find_all('div')[0].get_text(strip=True)
            draw_text = container.find_all('div')[1].get_text(strip=True)
            _logger.info(f"\n\n📅 Fecha encontrada: {date_text}\n\n")
            _logger.info(f"\n\n🎟️ Sorteo encontrado: {draw_text}\n\n")
            # Ejemplo: extraer el número desde "SORTEO #306"
            draw_number = None
            if 'SORTEO #' in draw_text:
                draw_number = int(draw_text.replace('SORTEO #', '').strip())
                _logger.info(f"\n\n🔢 Número de sorteo: {draw_number}\n\n")
                data = {
                    'date_text': date_text,
                    'draw_number': draw_number,
                    'game': game,
                }
                self._get_data(**data)
        except requests.exceptions.HTTPError as http_err:
            _logger.error(f"❌ Error HTTP al acceder a {url}: {http_err}")
            return
        except requests.exceptions.RequestException as req_err:
            _logger.error(f"❌ Error de conexión al acceder a {url}: {req_err}")
            return

    def _get_data(self, *args, **kwargs):
        date_text = kwargs.get('date_text')
        draw_number = kwargs.get('draw_number')
        url = f"{URLS['miloto']}/{draw_number}"
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            balls = soup.find_all('div', class_='yellow-ball')
            winning_numbers = [
                int(ball.text.strip())
                for ball in balls
                if ball.text.strip().isdigit()
            ]
            winning_info = self._extract_winning_info(soup)
            extract_acumulado = self._extract_acumulado(soup)
            _logger.info(
                f"\n\n\n\n {winning_numbers} {winning_info} "
                f"{extract_acumulado} \n\n"
            )
            draw_date = self._parse_draw_date(date_text)
            draw = self.env['lottery.draw'].create({
                'name': f"{kwargs.get('game').name} {date_text}",
                'draw_date': draw_date,
                'game_id': kwargs.get('game').id,
                'jackpot': float(extract_acumulado) or 0.0,
                "draw_number": int(draw_number),
                "win": winning_info['hay_ganador']
            })
            for i, num in enumerate(winning_numbers):
                self.env['lottery.draw.number'].create({
                    'draw_id': draw.id,
                    'number': int(num),
                    'color': int(4),
                })
        except requests.exceptions.RequestException as e:
            _logger.error(f"❌ Error al obtener datos de {url}: {e}")
            return

    def _extract_winning_info(self, soup):
        # 👉 Solo tomamos el primer bloque (aciertos 5)
        block = soup.find('div', class_='mt-4 bg-white rounded')
        if not block:
            return None
        try:
            aciertos = int(block.select_one(
                '.fs-aciertos strong'
            ).text.strip())
            premio_total = block.select_one('.fs-1.pink-light').text.strip()
            detalles = block.find(
                'div',
                style=lambda value: value and 'margin-top: -10px' in value
            )
            if not detalles:
                return None
            texto_detalles = detalles.get_text(separator=" ", strip=True)
            # Extraer valores numéricos del texto
            premio_ganador = re.search(
                r"Premio por ganador\s+\$[\d\.,]+", texto_detalles
            )
            ganadores = re.search(r"Ganadores\s+([\d\.,]+)", texto_detalles)
            premio_ganador_valor = (
                premio_ganador.group(0).split('$')[-1]
                if premio_ganador else "0"
            )
            ganadores_valor = ganadores.group(1) if ganadores else "0"
            return {
                "aciertos": aciertos,
                "premio_total": premio_total,
                "premio_por_ganador": premio_ganador_valor,
                "ganadores": int(
                    ganadores_valor.replace('.', '').replace(',', '')
                ),
                "hay_ganador": int(
                    ganadores_valor.replace('.', '').replace(',', '')
                ) > 0
            }
        except Exception as e:
            _logger.error(f"❌ Error al extraer info de ganadores: {e}")
            return None

    def _extract_acumulado(self, soup):
        acumulado_div = soup.find(
            'div',
            class_='text-center my-3 outfit-medium white-color fs-6'
        )
        if not acumulado_div:
            return None
        match = re.search(
            r"\$([\d\s\.]+)\s*MILLONES", acumulado_div.text.strip().upper()
        )
        if match:
            raw_amount = match.group(1)  # ejemplo: "120" o "1.200"
            # Removemos espacios y puntos, y convertimos a número
            clean_amount = raw_amount.replace('.', '').replace(' ', '')
            return float(clean_amount)
        return None

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
