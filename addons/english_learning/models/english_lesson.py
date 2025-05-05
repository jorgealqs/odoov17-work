from odoo import models, fields


class EnglishLesson(models.Model):
    _name = 'english.lesson'
    _description = 'English Lesson'

    name = fields.Char(
        string='Lesson Title',
        required=True
    )
    content = fields.Html(
        string='Lesson Content',
        help="HTML or Markdown-based content for the lesson."
    )
    media_url = fields.Char(
        string='Audio/Video URL',
        help="Optional audio or video URL for this lesson."
    )
    topic_id = fields.Many2one(
        'english.topic',
        string='Topic',
        required=True,
        ondelete='cascade'
    )
    exercise_ids = fields.One2many(
        'english.exercise',
        'lesson_id',
        string='Exercises'
    )