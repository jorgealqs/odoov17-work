from odoo import models, fields  # type: ignore
import logging

_logger = logging.getLogger(__name__)


class SportsCountry(models.Model):
    _name = 'sports.country'
    _description = 'Country Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Habilitar tracking

    name = fields.Char(string="Country Name", required=True, tracking=True)
    code = fields.Char(string="Country Code", tracking=True)
    flag = fields.Char(string="Flag URL", tracking=True)
    session_id = fields.Many2one(
        comodel_name='sports.session',
        string='Sessions',
        ondelete='restrict',
        tracking=True
    )

    def sync_leagues(self):
        model = self.env['sports.api.import']
        data = {
            'season': self.session_id.name,
            'code': self.code
        }
        model.fetch_leagues_from_api(**data)
