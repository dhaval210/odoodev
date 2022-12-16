{
    'name': 'Partner Ranking',
    'summary': 'RUN-1267',
    'description': """
        RUN-1267:https://jira.metrosystems.net/browse/RUN-1267,
        """,
    'version': '12.0.1.0.1',
    'author': 'Cybrosys for METRONOM GmbH',
    'category': 'Enhancement',
    'depends': [
        'base', 'metro_rungis_dashboard'
    ],
    'data': [
        'views/res_partner.xml',
    ],
    'license': 'Other proprietary',
    'installable': True,
}
