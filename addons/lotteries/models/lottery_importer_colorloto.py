from odoo import models, api
import requests
from bs4 import BeautifulSoup
import logging
import re
from .lottery_constants import (
    HEADERS,
    URLS
)  # 👈 importas las URLs
from datetime import datetime

_logger = logging.getLogger(__name__)


class LotteryImporterColorloto(models.AbstractModel):
    _name = 'lottery.importer.colorloto'
    _description = 'Importador de resultados ColorLoto'

    @api.model
    def run_import(self, game):
        url = game.website
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            sorteo_info = self._extract_sorteo_info(soup)
            lottery_data = self._extract_lottery_data(**sorteo_info)
            winner = self._has_winner_for_six_hits(soup)
            data = {
                "lottery_data": lottery_data,
                "game": game,
                "sorteo_info": sorteo_info,
                "winner": winner
            }
            self._create_lottery_draw(**data)
            _logger.info(f"\n\n\n{lottery_data}\n\n\n")
        except requests.exceptions.HTTPError as http_err:
            _logger.error(f"❌ Error HTTP al acceder a {url}: {http_err}")
            return
        except requests.exceptions.RequestException as req_err:
            _logger.error(f"❌ Error de conexión al acceder a {url}: {req_err}")
            return

    def _parse_draw_date(self, texto_fecha):
        _logger.info(f"\n\n\n _parse_draw_date {texto_fecha}\n\n\n")
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

        partes = texto_fecha
        for es, en in meses.items():
            if es in partes:
                partes = partes.replace(es, en)
                break
        return datetime.strptime(partes, "%d de %B de %Y").date()

    def _create_lottery_draw(self, *args, **kwargs):
        lottery_data = kwargs.get('lottery_data')
        acumulado = lottery_data.get('acumulado')
        results = lottery_data.get('results', [])
        game = kwargs.get('game')
        sorteo_info = kwargs.get('sorteo_info')
        date_text = sorteo_info.get('date_text')

        _logger.info(f"\n\n\n esto llegoo {date_text}\n\n\n")

        draw_number = sorteo_info.get('draw_number')
        draw_date = self._parse_draw_date(date_text)

        draw = self.env['lottery.draw'].create({
            'name': f"{game.name} {date_text}",
            'draw_date': draw_date,
            'game_id': game.id,
            'jackpot': float(acumulado) if acumulado else 0.0,
            "draw_number": int(draw_number),
            "win": kwargs.get('winner', False),
        })

        for result in results:
            number = int(result.get('number'))
            color_name = result.get('color')
            color_code = self._map_color_to_code(color_name)

            self.env['lottery.draw.number'].create({
                'draw_id': draw.id,
                'number': number,
                'color': color_code,
            })

    def _extract_sorteo_info(self, soup):
        # Busca el div específico
        div = soup.find('div', class_='white-color fs-3')
        if not div:
            return None, None

        text = div.text.strip()

        # Extrae el número del sorteo
        match_num = re.search(r"#(\d+)", text)
        draw_number = match_num.group(1) if match_num else None

        # Extrae la fecha
        match_fecha = re.search(
            r"-\s*(\d+\s+de\s+\w+\s+de\s+\d{4})", text, re.IGNORECASE
        )
        date_text = match_fecha.group(1) if match_fecha else None

        return {
            "draw_number": draw_number,
            "date_text": date_text
        }

    def _extract_lottery_data(self, *args, **kwargs):
        url = f"{URLS['colorloto']}/{kwargs.get('draw_number')}"
        _logger.info(f"\n\n\n{url} ---  {kwargs}\n\n\n")
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            html = response.content
        except requests.exceptions.HTTPError as http_err:
            _logger.error(f"❌ Error HTTP al acceder a {url}: {http_err}")
            return
        except requests.exceptions.RequestException as req_err:
            _logger.error(f"❌ Error de conexión al acceder a {url}: {req_err}")
            return

        soup = BeautifulSoup(html, "html.parser")

        # 🎯 1. Extraer el acumulado
        acumulado_div = soup.find('div', class_='fs-6')
        acumulado = None
        if acumulado_div:
            match = re.search(r"\$([\d\.]+)", acumulado_div.text)
            if match:
                acumulado = match.group(1).replace('.', '')  # "2.420" → "2420"

        # 🎯 2. Extraer números con colores
        results = []
        balotas = soup.select('div.balota')
        for balota in balotas:
            number = balota.text.strip()
            classes = balota.get('class', [])
            color = None
            for cls in classes:
                if cls.startswith('balota-') and cls != 'balota':
                    color = cls.replace('balota-', '')
            results.append({"number": number, "color": color})

        return {
            "acumulado": acumulado,
            "results": results
        }

    def _has_winner_for_six_hits(self, soup):
        """
        Verifica si hay ganadores con 6 aciertos exactos
        (sin NÚMEROS ni COLORES).
        Solo analiza la primera fila relevante.
        """
        row = soup.select_one('tr.results-row')
        if not row:
            return False

        aciertos_div = row.select_one('.success-number')
        if not aciertos_div or aciertos_div.text.strip() != "6":
            return False

        # Ignorar si tiene "NÚMEROS" o "COLORES"
        if "NÚMEROS" in row.text.upper() or "COLORES" in row.text.upper():
            return False

        celdas = row.find_all('td')
        if len(celdas) >= 3:
            ganadores_text = celdas[2].text.strip().replace(
                '.', ''
            ).replace(',', '')
            try:
                ganadores = int(ganadores_text)
                return ganadores > 0
            except ValueError:
                return False

        return False

    def _map_color_to_code(self, color_name):
        color_map = {
            "red": 1,
            "yellow": 2,
            "blue": 4,
            "green": 10,
            "white": 13,
            "black": 0,  # o None si prefieres dejar vacío
        }
        return color_map.get(color_name.lower(), 0)
