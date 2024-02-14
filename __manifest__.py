{
    'name': "Achievements",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'mail'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        # 'security/record_rules.xml',
        'views/achievements.xml',
        # 'wizard/report_wizard_views.xml',
    ],
    'demo': [],
    'summary': "Achievements",
    'description': "",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': True
}