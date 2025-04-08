{
    'name': 'Sports Betting',
    'version': '1.0',
    'sequence': -10,
    'category': 'OWN/SportsBetting',
    'summary': 'Manage sports betting operations and results tracking',
    'description': """
        Sports Betting Management System
        ==============================

        This module provides features for:
        * Managing different sports and leagues
        * Tracking betting odds and results
        * User bet management
        * Statistical analysis
        * Automated results verification
        * Financial tracking and reporting
    """,

    'author': 'Creative tech',
    'website': 'https://www.creativetech.com',
    'depends': [
        'base',
        'web',
        'mail'
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/sports_country_views.xml',
        'views/sports_session_views.xml',
        'views/sports_api_import_views.xml',
        'views/sports_league_views.xml',
        'views/sports_team_views.xml',
        'views/sports_team_views.xml',
        'views/sports_dashboard_views.xml',
        'data/data_sports_session.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sports_betting/static/src/**/*',
            ('remove', 'sports_betting/static/src/dashboard/**/*'),
        ],
        'sports_betting.dashboard': [
            'sports_betting/static/src/dashboard/**/*'
        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/banner.png'],
}
