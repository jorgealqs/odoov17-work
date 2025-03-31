import requests  # type: ignore
import logging
import os
from odoo import _  # type: ignore
from odoo.exceptions import UserError  # type: ignore

_logger = logging.getLogger(__name__)


class APIFootballHelper:
    """Helper class for handling API requests to Football API"""

    @staticmethod
    def get_api_headers():
        """Generate headers for API request"""
        return {
            'x-rapidapi-host': os.getenv('API_FOOTBALL_URL_V3'),
            'x-rapidapi-key': os.getenv('API_FOOTBALL_KEY')
        }

    @staticmethod
    def fetch_api_data(endpoint, params=None):
        """
        Fetch data from API Football with optional parameters.
        :param endpoint: API endpoint (e.g., '/leagues')
        :param params: Dictionary of parameters
        (e.g., {'code': 'CO', 'season': 2025})
        :return: JSON response data
        """
        base_url = os.getenv('API_FOOTBALL_URL')
        if not base_url:
            raise UserError(_("API URL is not configured."))

        url = f"{base_url}{endpoint}"
        response = requests.get(
            url,
            headers=APIFootballHelper.get_api_headers(), params=params
        )

        if response.status_code == 200:
            return response.json()
        else:
            _logger.error("Error fetching data from API: %s", response.text)
            raise UserError(
                _("Error fetching data from API: %s") % response.text
            )
