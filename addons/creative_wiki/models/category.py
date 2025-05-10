from odoo import models, fields


class KnowledgeCategory(models.Model):
    _name = 'knowledge.category'
    _description = 'Categoría de Conocimiento'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')

    _sql_constraints = [
        (
            'unique_name',
            'unique(name)',
            'The category name must be unique.')
    ]
