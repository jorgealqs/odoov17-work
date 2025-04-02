{
    "name": "Hide Powered By Odoo",
    "summary": "Removes the message 'Manage Databases Powered by Odoo'",
    "version": "1.0",
    'author': 'Jorge Alberto Quiroz Sierra',
    'category': 'OWN/RemoveLogin',
    'sequence': -40,
    "depends": ["web"],
    "data": [
        "views/login_template.xml",
    ],
    'assets': {},
    "installable": True,
    "auto_install": False,
    "application": False,
    'license': 'LGPL-3',
}
