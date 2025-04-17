# -*- coding: utf-8 -*-

import logging

from odoo import http  # type: ignore
from .services.dashboard_data import DashboardDataService
# 👈 Servicio separado

_logger = logging.getLogger(__name__)


class AwesomeDashboard(http.Controller):
    @http.route('/awesome_dashboard/statistics', type='json', auth='user')
    def get_statistics(self):
        """
        Endpoint que devuelve estadísticas para el dashboard.
        """
        return {
            "chart_data": DashboardDataService.get_dashboard_data_chart(),
            "leagues_data": DashboardDataService.get_active_country_league()
        }
