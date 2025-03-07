# -*- coding: utf-8 -*-
{
    'name': "Administración de Escuela",
    'application': True,
    'installable': True,
    'summary': """
        Módulo de Experimentación con diferentes conceptos y funcionalidades interesantes""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Ricardo Brenes",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Capacitación',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
    ],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
        #'demo/demo.xml',
    #],
}
