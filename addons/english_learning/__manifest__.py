{
    'name': 'English Learning',
    'version': '1.0',
    'sequence': -80,
    'category': 'OWN/English',
    'summary': 'English Leaning module',
    'author': 'Creative Tech',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/english_level_views.xml',
        'views/english_topic_views.xml',
        'views/english_lesson_views.xml',
        'views/english_exercise_views.xml',
        'views/english_song_views.xml',
        'views/english_song_exercises_views.xml',
        'views/english_dictionary_views.xml',
        'views/english_tag_views.xml',
        'views/english_phrase_views.xml',
        'data/cron.xml',
        'report/report.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3'
}
