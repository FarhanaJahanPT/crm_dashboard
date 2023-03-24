
{
    'name': 'CRM Dashboard',
    'sequence': 1,
    'version': '16.0.1.0.0',
    'depends': ['base', 'crm','sale'],
    'data': [
        'views/sales_team.xml',
        'views/dashboard_menu.xml',
    ],
    'assets': {
            'web.assets_backend': [
                'crm_dashboard/static/src/js/dashboard.js',
                'crm_dashboard/static/src/xml/dashboard.xml',
                'crm_dashboard/static/src/css/dashboard.scss',
                'https://cdn.jsdelivr.net/npm/chart.js',

            ]
        },
    'installable': True,
    'auto_install': False,
}