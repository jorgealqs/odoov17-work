from odoo import models, api
import logging
from .lottery_constants import SEARCH_BALOTO, SEARCH_MILOTO
from datetime import datetime

_logger = logging.getLogger(__name__)


class LotteryImporter(models.AbstractModel):
    _name = 'lottery.importer'
    _description = 'Lottery Importer Dispatcher'

    @api.model
    def run_import_baloto_revancha(self):
        """
        Run the import process for Baloto/Revancha only on Thursday and Sunday.
        """
        today = datetime.now().weekday()
        if today not in [3, 6]:  # Jueves = 3, Domingo = 6
            _logger.info("📅 Hoy no es día de importación de Baloto/Revancha.")
            return
        """Run the import process for all active lottery games."""
        lottery_games = self.env[
            'lottery.game'
        ].search(
            [
                ('name', 'in', SEARCH_BALOTO),
                ('active', '=', True)
            ]
        )
        _logger.info(
            f"🎯 Iniciando importación para {len(lottery_games)} juegos."
        )

        for game in lottery_games:
            importer_model = (
                "lottery.importer.baloto"
            )

            _logger.info(
                f"🔍 Buscando importador para: {game.name} → {importer_model}"
            )

            if importer_model in self.env:
                try:
                    self.env[importer_model].run_import(game)
                    _logger.info(f"✅ Importación exitosa para {game.name}")
                except Exception as e:
                    _logger.exception(
                        f"❌ Error al importar datos para {game.name}: {str(e)}"
                    )
            else:
                _logger.warning(
                    f"⚠️ No se encontró el importador para: {game.name}"
                )

    @api.model
    def run_import_miloto(self):
        """
        Run the import process for MiLoto only on Tuesday, Wednesday,
        Friday and Saturday.
        """
        today = datetime.datetime.now().weekday()
        if today not in [1, 2, 4, 5]:  # Martes, Miércoles, Viernes, Sábado
            _logger.info("📅 Hoy no es día de importación de MiLoto.")
            return
        """Run the import process for all active lottery games."""
        lottery_games = self.env[
            'lottery.game'
        ].search(
            [
                ('name', 'in', SEARCH_MILOTO),
                ('active', '=', True)
            ]
        )
        _logger.info(
            f"🎯 Iniciando importación para {len(lottery_games)} juegos."
        )

        for game in lottery_games:
            try:
                self.env['lottery.importer.miloto'].run_import(game)
                _logger.info(f"✅ Importación exitosa para {game.name}")
            except Exception as e:
                _logger.exception(
                    f"❌ Error al importar datos para {game.name}: {str(e)}"
                )
            _logger.info(f"🔍 Buscando importador para: {game.name}")
