import logging
from odoo.http import request

_logger = logging.getLogger(__name__)


def _get_name_dict(model_name):
    records = request.env[model_name].search_read([], ['name'])
    return {rec['id']: rec['name'] for rec in records}


def _replace_ids_with_names(records, tag_dict, category_dict):
    for rec in records:
        rec['tag_ids'] = [(tag_id, tag_dict.get(tag_id)) for tag_id in rec.get('tag_ids', [])]
        if rec.get('category_id'):
            cat_id = rec['category_id'][0]
            rec['category_id'] = (cat_id, category_dict.get(cat_id))
    return records


def get_notes():
    notes = request.env['knowledge.note'].search_read([], [])

    tag_dict = _get_name_dict('knowledge.tag')
    category_dict = _get_name_dict('knowledge.category')

    return _replace_ids_with_names(notes, tag_dict, category_dict)


def get_resources():
    resources = request.env['knowledge.resource'].search_read([], ['name', 'url', 'description', 'category_id', 'tag_ids'])

    tag_dict = _get_name_dict('knowledge.tag')
    category_dict = _get_name_dict('knowledge.category')

    return _replace_ids_with_names(resources, tag_dict, category_dict)