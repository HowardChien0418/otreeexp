from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.10, participation_fee=0.00, doc=""
)


SESSION_CONFIGS = [
    dict(
        name='red_line_experiment',
        display_name='Red Line Experiment',
        num_demo_participants=4,
        participation_fee=5.00,
        real_world_currency_per_point=0.10,
        app_sequence=[
            'red_line_experiment',
            'red_line_lottery',
            'red_line_demographic_survey'
        ]
    )
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='ssel nyuad',
        participant_label_file='_rooms/ssel.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Welcome!
"""

# don't share this with anybody.
SECRET_KEY = '9g!-yrk!f3o%=%^cp=f#bl6qsoct$=6+nms@3d&t5djgro5v2$'

INSTALLED_APPS = ['otree']
