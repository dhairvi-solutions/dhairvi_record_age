# -*- coding: utf-8 -*-
# Copyright 2026 Dhairvi Solutions LLP
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
{
    'name': 'Dhairvi Record Age',
    'version': '19.0.1.0.1',
    'category': 'Productivity',
    'summary': 'Show calendar days since an Odoo record was created',
    'description': 'Adds a computed Record Age field (calendar days since create_date).',
    'author': 'Dhairvi Solutions LLP',
    'website': 'https://www.dhairvi.com',
    'support': 'info@dhairvi.com',
    'license': 'LGPL-3',
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    'depends': ['base'],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 60,
}
