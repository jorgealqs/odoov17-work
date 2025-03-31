from odoo import models, fields  # type: ignore


class SportsSession(models.Model):
    _name = 'sports.session'
    _description = 'Sports Session'

    name = fields.Integer(string="Session Number", required=True)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The session number must be unique!')
    ]
