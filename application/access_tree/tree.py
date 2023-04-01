from pbac import Group, Policy, Rule, Algorithm, Subject, Target, Effect, Context, Action, Actions

from application.logic.models import *


access_tree = Group(
    _id='core',
    description='core-group',
    algorithm=Algorithm.DENY_UNLESS_PERMIT,
    items=[
        Policy(
            _id='admin',
            description='Корневая политика админа.',
            algorithm=Algorithm.PERMIT_UNLESS_DENY,
            actors=Subject == User,
            condition=Subject.role == 'admin',
            rules=[],
        ),
        Group(
            _id='user',
            description='Корневая группа юзеров.',
            algorithm=Algorithm.DENY_UNLESS_PERMIT,
            actors=Subject == User,
            items=[
                Group(
                    _id='simple-user',
                    description='Группа простых юзеров.',
                    algorithm=Algorithm.DENY_UNLESS_PERMIT,
                    condition=Subject.role == 'simple',
                    items=[
                        Policy(
                            _id='product-access',
                            description='Политика доступа к продуктам.',
                            algorithm=Algorithm.PERMIT_UNLESS_DENY,
                            condition=Target == Product,
                            rules=[
                                Rule(
                                    _id='product-read-only-allowed',
                                    description='Запретить чтение продуктов, к которым нет доступа.',
                                    effect=Effect.DENY,
                                    condition=(
                                        Action == Actions.READ
                                        and (Subject.id != Product.owner_id)
                                        and (Context.provided.target_owner_settings.share_products == False)
                                    )
                                ),
                                Rule(
                                    _id='product-update-only-allowed',
                                    description='Запретить обновление не своих продуктов.',
                                    effect=Effect.DENY,
                                    condition=(Action == Actions.UPDATE) and (Subject.id != Product.owner_id)
                                ),
                                Rule(
                                    _id='product-delete-only-allowed',
                                    description='Запретить обновление не своих продуктов.',
                                    effect=Effect.DENY,
                                    condition=(Action == Actions.DELETE) and (Subject.id != Product.owner_id)
                                ),
                            ],
                        ),
                        Policy(
                            _id='product-record-access',
                            description='Политика доступа к записям продуктов.',
                            algorithm=Algorithm.PERMIT_UNLESS_DENY,
                            condition=Target == ProductRecord,
                            rules=[
                                Rule(
                                    _id='product-record-read-only-allowed',
                                    description='Запретить чтение записей продуктов, к которым нет доступа.',
                                    effect=Effect.DENY,
                                    condition=(
                                        (Action == Actions.READ)
                                        and (Subject.id != Target.owner_id)
                                    )
                                ),
                                Rule(
                                    _id='product-record-update-only-allowed',
                                    description='Запретить обновление не своих записей продуктов.',
                                    effect=Effect.DENY,
                                    condition=(Action == Actions.UPDATE) and (Subject.id != Product.owner_id)
                                ),
                                Rule(
                                    _id='product-record-delete-only-allowed',
                                    description='Запретить обновление не своих записей продуктов.',
                                    effect=Effect.DENY,
                                    condition=(Action == Actions.DELETE) and (Subject.id != Product.owner_id)
                                ),
                            ],
                        ),
                        Policy(
                            _id='user-settings-access',
                            description='Политика доступа к настройках пользователя.',
                            algorithm=Algorithm.PERMIT_UNLESS_DENY,
                            condition=Target == UserSettings,
                            rules=[
                                Rule(
                                    _id='user-settings-allow-only-owned',
                                    description='Запретить любой доступ не к своим настройкам.',
                                    effect=Effect.DENY,
                                    condition=(
                                        (Action == Actions.READ)
                                        or (Action == Actions.UPDATE)
                                        and (Subject.id != UserSettings.owner_id)
                                    )
                                ),
                                Rule(
                                    _id='user-settings-forbid-writting-and-deletion',
                                    description='Запретить создание и удаление настроек.',
                                    effect=Effect.DENY,
                                    condition=(Action == Actions.DELETE) and (Action == Actions.WRITE)
                                )
                            ],
                        )
                    ]
                )
            ]
        )
    ]
)