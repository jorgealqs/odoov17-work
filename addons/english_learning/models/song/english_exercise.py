from odoo import models, fields


class EnglishExercise(models.Model):
    _name = 'english.exercise.song'
    _description = 'Exercise Based on Song'

    name = fields.Char(string="Exercise Name")
    description = fields.Text(string="Instructions")
    song_id = fields.Many2one(
        'english.song',
        string="Song"
    )
    exercise_type = fields.Selection([
        ('fill_gap', 'Fill in the Gaps'),
        ('translate', 'Translate'),
        ('questions', 'Comprehension Questions'),
    ], string="Type")
