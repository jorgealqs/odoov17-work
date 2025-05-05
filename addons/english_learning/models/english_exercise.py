from odoo import models, fields


class EnglishExercise(models.Model):
    _name = 'english.exercise'
    _description = 'English Exercise'

    question = fields.Text(
        string='Question / Instruction',
        required=True
    )
    option_a = fields.Char(string='Option A')
    option_b = fields.Char(string='Option B')
    option_c = fields.Char(string='Option C')
    option_d = fields.Char(string='Option D')
    correct_answer = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
    ], string='Correct Answer')
    type_question = fields.Selection([
        ('multiple_choice', 'Multiple Choice'),
        ('order_sentence', 'Order Sentence'),
        ('true_false', 'True/False'),
    ], string='Type of Exercise', default='multiple_choice')
    lesson_id = fields.Many2one(
        'english.lesson',
        string='Related Lesson',
        required=True,
        ondelete='cascade'
    )