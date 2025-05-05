from odoo import models, fields


class EnglishLevel(models.Model):
    _name = 'english.level'
    _description = 'English Level'

    LEVEL_OPTIONS = [
        ('a1', 'A1 - Beginner'),
        ('a2', 'A2 - Elementary'),
        ('b1', 'B1 - Intermediate'),
        ('b2', 'B2 - Upper Intermediate'),
        ('c1', 'C1 - Advanced'),
        ('c2', 'C2 - Proficient'),
    ]

    name = fields.Selection(selection=LEVEL_OPTIONS, string='Level', required=True)
    description = fields.Html(string='General Description')
    topic_ids = fields.One2many(
        'english.topic',
        'level_id',
        string='Topics'
    )

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The level must be unique.')
    ]