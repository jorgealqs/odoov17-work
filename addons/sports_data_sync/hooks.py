import csv
import os
import logging

_logger = logging.getLogger(__name__)


def _import_countries(env):
    _logger.info("🗺️ Importing countries into sports.track.country")
    file_path = os.path.join(os.path.dirname(__file__), 'data/countries.csv')
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name'] and row['Flag']:
                env['sports.track.country'].create({
                    'name': row['Name'],
                    'continent': row['Continent'],
                    'country_code': row['Country Code'],
                    'flag': row['Flag'],
                })
