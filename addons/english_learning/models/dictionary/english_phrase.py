from odoo import models, fields  # type: ignore


class LearningPhrase(models.Model):
    _name = 'english.phrase'
    _description = 'Learning Phrase'

    name = fields.Char(string='Phrase', required=True)
    context = fields.Text(string='Usage / Explanation')
    sequence = fields.Integer(string='Sequence', default=10)
    tag_ids = fields.Many2many('english.tag', string="Tags")
