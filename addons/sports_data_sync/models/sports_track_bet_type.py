from odoo import models, fields  # type: ignore
import logging

_logger = logging.getLogger(__name__)


class SportsTrackBetType(models.Model):
    _name = 'sports.track.bet.type'
    _description = 'Bet Type'
    _order = "name"

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The name must be unique.')
    ]
