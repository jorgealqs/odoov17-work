from odoo import models, fields


class EnglishExerciseSongQuestion(models.Model):
    _name = 'english.exercise.song.question'
    _description = 'Question for Song Exercise'

    exercise_id = fields.Many2one(
        'english.exercise.song',
        string="Exercise",
        required=True,
        ondelete='cascade'
    )
    question_text = fields.Text(string="Question", required=True)
    question_type = fields.Selection([
        ('open', 'Open-ended'),
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
    ], string="Question Type", required=True)
    options = fields.Text(
        string="Options (if multiple choice)",
        help="Separate options with | (pipe character)"
    )
    correct_answer = fields.Char(string="Correct Answer")
    feedback = fields.Text(string="Feedback / Explanation (optional)")