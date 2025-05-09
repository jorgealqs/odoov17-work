from odoo import models, fields


class EnglishTag(models.Model):
    _name = 'english.tag'
    _description = 'English Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')

    _sql_constraints = [
        (
            'check_name',
            'UNIQUE(name)',
            'The name is unique!!!',
        )
    ]
