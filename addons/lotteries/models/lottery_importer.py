from odoo import models, api
import logging
from .lottery_constants import (
    SEARCH_BALOTO,
    SEARCH_MILOTO,
    SEARCH_COLORLOTO,
    SEARCH_MEDELLIN
)
from datetime import datetime

_logger = logging.getLogger(__name__)


class LotteryImporter(models.AbstractModel):
    _name = 'lottery.importer'
    _description = 'Lottery Importer Dispatcher'

    def _import_lotteries(
        self,
        search_names,
        importer_model_name,
        allowed_days=None
    ):
        """
        Método reutilizable para importar sorteos de loterías.

        :param search_names: Lista de nombres de juegos a buscar
        (e.g. SEARCH_BALOTO)
        :param importer_model_name: Nombre del modelo importador (str)
        :param allowed_days: Lista de días permitidos para importar (opcional)
        """
        today = datetime.now().weekday()

        if allowed_days and today not in allowed_days:
            _logger.info(
                f"📅 Hoy no es día permitido para importar ."
                f"{importer_model_name}."
            )
            return

        lottery_games = self.env['lottery.game'].search([
            ('name', 'in', search_names),
            ('active', '=', True)
        ])

        _logger.info(
            f"🎯 Iniciando importación para "
            f"{len(lottery_games)} juegos con importador {importer_model_name}"
        )

        for game in lottery_games:
            _logger.info(
                f"🔍 Buscando importador para: {game.name} → "
                f"{importer_model_name}"
            )
            if importer_model_name in self.env:
                try:
                    self.env[importer_model_name].run_import(game)
                    _logger.info(f"✅ Importación exitosa para {game.name}")
                except Exception as e:
                    _logger.exception(
                        f"❌ Error al importar datos para {game.name}: {str(e)}"
                    )
            else:
                _logger.warning(
                    f"⚠️ No se encontró el importador: {importer_model_name}"
                )

    @api.model
    def run_import_baloto_revancha(self):
        self._import_lotteries(
            SEARCH_BALOTO,
            'lottery.importer.baloto',
            allowed_days=[3, 6]  # Jueves y Domingo
        )

    @api.model
    def run_import_miloto(self):
        self._import_lotteries(
            SEARCH_MILOTO,
            'lottery.importer.miloto',
            allowed_days=[1, 2, 4, 5]  # Martes, Miércoles, Viernes, Sábado
        )

    @api.model
    def run_import_colorloto(self):
        self._import_lotteries(
            SEARCH_COLORLOTO,
            'lottery.importer.colorloto',
            allowed_days=[1, 4]  # Martes, Viernes
        )

    @api.model
    def run_import_medellin(self):
        self._import_lotteries(
            SEARCH_MEDELLIN,
            'lottery.importer.medellin',
            allowed_days=[5]  # Sabado
        )
