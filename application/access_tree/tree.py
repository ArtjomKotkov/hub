from pbac import Group, Policy, Rule, Algorithm, Subject

from application.logic.models import *


access_tree = Group(
    _id='core',
    description='core-group',
    algorithm=Algorithm.DENY_UNLESS_PERMIT,
    items=[
        Policy(
            _id='admin',
            description='admin-policy',
            algorithm=Algorithm.PERMIT_UNLESS_DENY,
            actors=Subject == User,
            condition=Subject.role == 'admin',
            rules=[],
        )
    ]
)