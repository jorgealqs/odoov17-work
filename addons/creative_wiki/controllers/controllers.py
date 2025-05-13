# -*- coding: utf-8 -*-

import logging
from odoo import http
from .services.dashboard import (
    get_notes,
    get_resources
)

_logger = logging.getLogger(__name__)


class WikiKnowledgeController(http.Controller):
    @http.route('/wiki/resources', type='json', auth='user')
    def get_resources_wiki(self, **kw):
        try:
            return {
                'notes': get_notes(),
                'resources': get_resources(),
            }
        except Exception as e:
            _logger.error(f"Error fetching sports data: {str(e)}")
            return {
                'status': 'error',
                'message': 'Failed to fetch sports data',
            }
