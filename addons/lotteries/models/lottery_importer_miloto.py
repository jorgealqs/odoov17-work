from odoo import models, api  # type: ignore
import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
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
        latest_draw = self.env['lottery.draw'].search(
            [("game_id", "=", game.id)],
            order='draw_number desc',
            limit=1
        )
        draw_number = latest_draw.draw_number if latest_draw else 0

        data = {
            'draw_number': int(draw_number) + 1,
            'game': game,
        }
        self._get_data(**data)

    def _get_data(self, *args, **kwargs):
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
            date_div = soup.find('div', class_='fs-5')
            date_text = date_div.get_text(strip=True) if date_div else None
            _logger.info(
                f"\n\n\n {date_text} \n\n"
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

        for es, en in meses.items():
            if es in texto_fecha:
                texto_fecha = texto_fecha.replace(es, en)
                break

        return datetime.strptime(texto_fecha, "%d de %B de %Y").date()
