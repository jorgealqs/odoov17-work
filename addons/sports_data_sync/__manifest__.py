{
    'name': 'Sports Data Sync',
    'version': '1.0',
    'sequence': -70,
    'category': 'OWN/Sports',
    'summary': "Sync football data (countries, leagues, teams) and"
    "generate statistics & forecasts.",
    'description': """
Sports Data Sync
=================
Este módulo permite sincronizar información deportiva desde fuentes externas
(como API-Football) incluyendo:
- Países
- Ligas
- Equipos
Además de mostrar estadísticas y generar pronósticos
(forecasting) personalizados.
""",
    'author': 'Creative Tech',
    'website': 'https://creativetech.dev',
    'depends': [
        'base',
        'web',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        "data/data_session.xml",
        'views/dashboard.xml',
        'views/country_views.xml',
        'views/league_views.xml',
        'views/team_views.xml',
        'views/standing_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'assets': {
        'web.assets_backend': [
            'sports_data_sync/static/src/**/*',
            ('remove', 'sports_data_sync/static/src/dashboard/**/*'),
        ],
        'sports_sync_data.dashboard': [
            'sports_data_sync/static/src/**/*'
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'post_init_hook': '_import_countries',
    'license': 'LGPL-3'
}
