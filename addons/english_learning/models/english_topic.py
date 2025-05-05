from odoo import models, fields


class EnglishTopic(models.Model):
    _name = 'english.topic'
    _description = 'English Topic'

    name = fields.Char(string='Topic Name', required=True)  # Example: Modal Verbs, Food
    description = fields.Html(string='Topic Description')
    level_id = fields.Many2one('english.level', string='Level')

    # New One2many field
    lesson_ids = fields.One2many(
        'english.lesson',
        'topic_id',
        string='Lessons'
    )

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The level must be unique.')
    ]