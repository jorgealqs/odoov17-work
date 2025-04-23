import logging
from odoo import models, fields
from datetime import datetime
import pytz
import requests

_logger = logging.getLogger(__name__)


class CryptoPriceHistory(models.Model):
    _name = 'crypto.price.history'
    _description = "Crypto Price History"
    _order = "timestamp desc"

    coin_id = fields.Many2one(
        "crypto.coin", string="Cryptocurrency", required=True
    )
    usd = fields.Float()
    cop = fields.Float()
    timestamp = fields.Datetime(string="Timestamp", required=True)

    def fetch_and_save_crypto_prices(self):
        """Save the current price history for followed coins."""
        Crypto = self.env['crypto.coin']
        # Step 1: Fetch followed coins
        followed_coins = Crypto.search([("follow", "=", True)])
        if not followed_coins:
            _logger.info("No followed coins found.")
            return {"coins": []}
        # Step 2: Prepare CoinGecko API query
        coin_ids = ",".join([
            coin.name.lower() for coin in followed_coins if coin.name
        ])
        if not coin_ids:
            _logger.warning("No valid coin names found for API query.")
            return {"coins": []}
        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            f"?ids={coin_ids}&vs_currencies=usd,cop"
        )
        # Step 3: Request prices from API
        try:
            response = requests.get(url)
            response.raise_for_status()
            prices = response.json()
        except Exception as e:
            _logger.error(f"Error fetching prices from CoinGecko API: {e}")
            return {"coins": []}
        # Step 5: Process each followed coin
        for coin in followed_coins:
            slug = coin.name.lower()
            price_info = prices.get(slug, {})
            usd_price = price_info.get("usd", 0)
            cop_price = price_info.get("cop", 0)
            now_utc = datetime.now(pytz.utc).replace(tzinfo=None)
            # Store in history
            self.create({
                "coin_id": coin.id,
                "usd": usd_price,
                "cop": cop_price,
                "timestamp": now_utc,
            })
