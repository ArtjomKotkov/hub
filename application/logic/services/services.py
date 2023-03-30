from dependency_injector import containers, providers

from settings import Settings

from .user import UserService
from .tokens import TokensService
from .auth import AuthService
from .telegram import TelegramExternalService, TelegramWebhookService
from .product_record import ProductRecordService
from .products import ProductsService
from .user_settings import UserSettingsService

from ..repositories import MemoryRepository


class Services(containers.DeclarativeContainer):
    user_repo = MemoryRepository(primary_key='id')

    user_settings = providers.Factory(
        UserSettingsService,
        user_settings_repo=MemoryRepository(primary_key='id'),
    )

    user = providers.Factory(
        UserService,
        user_repo=user_repo,
    )

    tokens = providers.Factory(
        TokensService,
        auth_token_repo=MemoryRepository(primary_key='token'),
        refresh_token_repo=MemoryRepository(primary_key='refresh_token'),
        user_repo=user_repo,
    )

    external_telegram = providers.Factory(
        TelegramExternalService,
        bot_token=Settings.TELEGRAM_BOT_TOKEN,
        callback_url=Settings.TELEGRAM_WEBHOOK_CALLBACK_RUL,
        webhook_secret=Settings.TELEGRAM_WEBHOOK_SECRET,
    )

    webhook_telegram = providers.Factory(
        TelegramWebhookService,
    )

    auth_service = providers.Factory(
        AuthService,
        tokens_service=tokens,
        telegram_service=external_telegram,
        user_service=user,
        auth_bot_token=Settings.TELEGRAM_BOT_TOKEN,
    )

    products_repo = MemoryRepository(primary_key='id')

    products_service = providers.Factory(
        ProductsService,
        products_repo=products_repo
    )

    prodict_record_service = providers.Factory(
        ProductRecordService,
        product_record_repo=MemoryRepository(primary_key='id'),
        products_repo=products_repo,
    )
