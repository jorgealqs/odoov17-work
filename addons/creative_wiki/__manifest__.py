{
    'name': 'Creative Wiki',
    'version': '1.0',
    'sequence': -90,
    'category': 'OWN/Wiki',
    'summary': 'Wiki and personal finance',
    'author': 'Creative Tech',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/knowledge_category_views.xml',
        'views/knowledge_resource_views.xml',
        'views/knowledge_note_views.xml',
        'views/knowledge_tag_views.xml',
        'views/menu.xml',
        # 'data/demo.xml',
        # 'report/report.xml',
        # 'wizard/wizard.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3'
}
