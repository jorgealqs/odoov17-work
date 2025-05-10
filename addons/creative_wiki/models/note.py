from odoo import models, fields


class KnowledgeNote(models.Model):
    _name = 'knowledge.note'
    _description = 'Personal note or idea'

    name = fields.Char(string='Title', required=True)
    content = fields.Html(string='Content')
    category_id = fields.Many2one(
        'knowledge.category',
        string='Category'
    )
    type_note = fields.Selection([
        ('idea', 'Idea'),
        ('note', 'Note'),
        ('blog_draft', 'Draft blog'),
        ('log', 'Logbook'),
    ], string='Type', default='note')
    tag_ids = fields.Many2many(
        'knowledge.tag',
        string="Tags"
    )

    _sql_constraints = [
        (
            'unique_name',
            'unique(name)',
            'The category name must be unique.')
    ]
