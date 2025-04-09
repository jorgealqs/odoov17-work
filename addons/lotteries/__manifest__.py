{
    'name': 'Lotteries Module',
    'version': '1.0',
    'sequence': -50,
    'category': 'OWN/Lotteries',
    'summary': 'Manage lotteries and their results',
    'description': """
        Lottery Management System
        ========================
        - Manage different types of lotteries
        - Track lottery results
        - Generate reports and statistics
        - Handle winners and prizes
    """,
    'author': 'Creative Tech',
    'website': 'https://www.creativetech.com',
    'depends': [
        'base',
        'mail',
        'web'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/lottery_games_views.xml',
        'views/lottery_draw_views.xml',
        'data/cron.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3'
}
