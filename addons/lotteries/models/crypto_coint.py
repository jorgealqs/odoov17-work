import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class CryptoCoin(models.Model):
    _name = 'crypto.coin'
    _description = 'Criptomoneda'

    name = fields.Char(string='Nombre', required=True)
    symbol = fields.Char(string='Símbolo', required=True)
    follow = fields.Boolean(string='Activo', default=False)
    logo = fields.Char(string='Logo')

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            'El nombre de la criptomoneda debe ser único!'
        )
    ]
