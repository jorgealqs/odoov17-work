from odoo import models, fields, exceptions
import logging

_logger = logging.getLogger(__name__)


class SportsTrackCountry(models.Model):
    _name = 'sports.track.country'
    _description = 'Sports Track Country'
    _order = "name"

    name = fields.Char(string='Name', required=True)
    country_code = fields.Char(string='Country Code')
    flag = fields.Char(string='Flag')
    continent = fields.Char(string='Continent')
    session_id = fields.Many2one(
        'sports.track.session',
        string='Sessions',
        ondelete='restrict'
    )

    def sync_leagues(self):
        for country in self:
            if not country.session_id:
                raise exceptions.UserError(
                    "No session found for this country."
                )
            data = {
                'country': {
                    'id': country.id,
                    'name': country.name,
                    'country_code': country.country_code,
                },
                'session': {
                    'id': country.session_id.id,
                    'year': country.session_id.year,
                }
            }
            self.env['sports.track.league']._sync_leagues(**data)
