# -*- coding: utf-8 -*-
{
    'name': "Real Estate",
    'application': True,
    'summary': """
        Test Module Beforte the Real App """,

    'description': """

    """,

    'author': "Ricardo Brenes",
    'website': "https://www.coromuni.go.cr",

    'category': 'P.D.I.',
    'version': '16.0.1.0.0',

    'depends': [
    ],

    'data': [
        #'security/groups.xml',
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
    ]
}
