# Copyright 2011- Minorisa, S.L. <http://www.minorisa.net>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Minorisa Development',
    'summary': 'Development Utilities',
    'category': 'Extra Tools',
    'images': [],
    'version': '12.0.0.2.0',
    'author': 'Minorisa SA',
    'support': 'projectes-odoo@minorisa.net',
    'website': 'https://www.minorisa.net',
    'license': 'GPL-3',
    'depends': [],
    'data': [
        # Security
        'security/groups.xml',
        # 'security/ir.model.access.csv',
        # Root menu
        'views/min_dev_menu.xml',
        # Menu
        'views/menu.xml',
        'views/group.xml',
        'views/download_translations_view.xml',
        'views/delete_attachments_views.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
}
