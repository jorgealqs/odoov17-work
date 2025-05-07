{
    'name': 'Inheritance Contacts',
    'version': '1.0',
    'sequence': -90,
    'category': 'OWN/Inheritence',
    'summary': 'Contacts app.',
    'description': """
This module extends the Contacts app.
""",
    'author': 'Creative Tech',
    'website': 'https://creativetech.dev',
    'depends': [
        'base',
        'web',
        'english_learning',
        'lotteries',
        'sports_data_sync'
    ],
    'data': [
        # XML files like views, security, reports go here
        'views/res_partner.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'inherit_contacts/static/src/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}