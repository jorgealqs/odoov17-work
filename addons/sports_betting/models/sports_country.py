from odoo import models, fields  # type: ignore


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
