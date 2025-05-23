{
    'name': 'CV Manager',
    'version': '1.0',
    'summary': 'Manage and download CVs in PDF',
    'description': 'A module to manage CVs and download them in PDF format.',
    'author': 'Jorge Alberto Quiroz Sierra',
    'category': 'OWN/CV',
    'sequence': -30,
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'reports/cv_report.xml',
        'reports/cv_report_vitae.xml',
        'views/curriculum_views.xml',
        'views/cv_education_views.xml',
        'views/menu.xml',
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    'license': 'LGPL-3',
}
