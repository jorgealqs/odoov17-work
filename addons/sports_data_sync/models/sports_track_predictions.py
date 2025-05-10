import logging
from time import sleep
from odoo import models, fields
from .api_football_connector import APIFootballConnector
from datetime import datetime
from ..controllers.services.dashboard import get_rounds_leagues

_logger = logging.getLogger(__name__)

class SportsTrackPredictions(models.Model):
    _name = 'sports.track.predictions'
    _description = 'Football Track Predictions'


    fixture_id = fields.Many2one(
        'sports.track.fixture',
        string="Fixture",
        required=True
    )
    winner = fields.Char(string="Predicted Winner")
    win_or_draw = fields.Boolean(string="Win or Draw")
    under_over = fields.Char(string="Under/Over")

    goals_home = fields.Char(string="Goals Home")
    goals_away = fields.Char(string="Goals Away")

    advice = fields.Text(string="Advice")

    percent_home = fields.Char(string="Home Win %")
    percent_draw = fields.Char(string="Draw %")
    percent_away = fields.Char(string="Away Win %")


    def sync_predictions(self):
        fixture_ids = get_rounds_leagues(True)
        for fixture_id in fixture_ids:
            id_table = fixture_id.get('id')
            fixture_api_id = fixture_id.get('fixture_api_id')
            # Verifica si ya existe una predicción para este fixture_id
            existing = self.search([('fixture_id', '=', fixture_api_id)], limit=1)
            if existing:
                _logger.info(f"Predicción ya existe para fixture_id {fixture_id}. Saltando...")
                continue
            connector = APIFootballConnector()
            res_predictions = connector.get_prediction(int(fixture_api_id))
            for res in res_predictions:
                prediction = res['predictions']
                vals_prediction = {
                    'fixture_id': id_table,
                    'winner': prediction.get('winner', {}).get('name'),
                    'win_or_draw': prediction.get('win_or_draw'),
                    'under_over': prediction.get('under_over'),
                    'goals_home': prediction.get('goals', {}).get('home'),
                    'goals_away': prediction.get('goals', {}).get('away'),
                    'advice': prediction.get('advice'),
                    'percent_home': prediction.get('percent', {}).get('home'),
                    'percent_draw': prediction.get('percent', {}).get('draw'),
                    'percent_away': prediction.get('percent', {}).get('away'),
                }
                _logger.info(f"\n\n {fixture_id} -- {vals_prediction} \n\n")
                self.create(vals_prediction)
                sleep(9)
