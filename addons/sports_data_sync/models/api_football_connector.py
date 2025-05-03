import os
import logging
import requests  # type: ignore
from requests.exceptions import RequestException  # type: ignore

_logger = logging.getLogger(__name__)


class APIFootballConnector:
    def __init__(self):
        self.base_url = os.getenv('API_FOOTBALL_URL')
        self.api_host = os.getenv('API_FOOTBALL_URL_V3')
        self.api_key = os.getenv('API_FOOTBALL_KEY')
        self.headers = {
            'x-rapidapi-host': self.api_host,
            'x-rapidapi-key': self.api_key
        }

    def _make_request(self, endpoint: str, params: dict = None):
        url = f'{self.base_url}/{endpoint}'
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json().get('response', [])
        except RequestException as e:
            _logger.error(
                f"API Request failed: {url} | Params: {params} | Error: {e}"
            )
            return []

    def get_leagues(self, country_name: str, country_code: str, season: int):
        if country_name.lower() == 'world':
            params = {'country': country_name, 'season': season}
        else:
            params = {'code': country_code, 'season': season}
        return self._make_request('leagues', params)

    def get_standings(self, league_id: int, season: int):
        params = {'league': league_id, 'season': season}
        return self._make_request('standings', params)

    def get_fixtures(self, league_id: int, season: int):
        params = {
            'league': league_id,
            'season': season,
            'timezone': "America/Bogota"
        }
        return self._make_request('fixtures', params)

    def get_prediction(self, prediction_id: int):
        params = {
            'fixture': prediction_id,
        }
        return self._make_request('predictions', params)
