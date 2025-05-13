{
    'name': 'Creative Wiki',
    'version': '1.0',
    'sequence': -90,
    'category': 'OWN/Wiki',
    'summary': 'Wiki and personal finance',
    'author': 'Creative Tech',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/knowledge_category_views.xml',
        'views/knowledge_resource_views.xml',
        'views/knowledge_note_views.xml',
        'views/knowledge_tag_views.xml',
        'views/action_dashboard.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'creative_wiki/static/src/**/*',
            ('remove', 'creative_wiki/static/src/dashboard/**/*'),
        ],
        'creative_wiki_knowledge.dashboard': [
            'creative_wiki/static/src/**/*'
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3'
}
