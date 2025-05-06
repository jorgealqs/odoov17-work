from odoo import models, fields


class EnglishExercise(models.Model):
    _name = 'english.exercise.song'
    _description = 'Exercise Based on Song'

    name = fields.Char(
        string="Exercise Name",
        required=True
    )
    description = fields.Html(string="Instructions")
    song_id = fields.Many2one(
        'english.song',
        string="Song",
        required=True
    )
    exercise_type = fields.Selection([
        ('fill_gap', 'Fill in the Gaps'),
        ('translate', 'Translate'),
        ('questions', 'Comprehension Questions'),
    ], string="Type", required=True)
    estimated_time = fields.Integer(
        string="Estimated Time (minutes)"
    )
    question_ids = fields.One2many(
        'english.exercise.song.question',
        'exercise_id',
        string="Questions"
    )
    tags = fields.Char(
        string="Tags",
        help="Comma-separated tags (e.g. emotions, daily routine, metaphors)"
    )