from odoo import models, fields  # type: ignore
import logging

_logger = logging.getLogger(__name__)


class SportsTrackBookmaker(models.Model):
    _name = 'sports.track.bookmaker'
    _description = 'Bookmaker (Betting House)'
    _order = "name"

    name = fields.Char(string='Name', required=True)
    website = fields.Char(string='Website')
    country = fields.Many2one(
        'sports.track.country'
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The name must be unique.')
    ]
