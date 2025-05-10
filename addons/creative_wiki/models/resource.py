from odoo import models, fields


class KnowledgeResource(models.Model):
    _name = 'knowledge.resource'
    _description = '(link, video, article)'

    name = fields.Char(string='Title', required=True)
    url = fields.Char(string='Url')
    description = fields.Html(string='Description')
    category_id = fields.Many2one(
        'knowledge.category',
        string='Category'
    )
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
