from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, Depends, Request

from application.logic import TelegramWebhookService, TelegramUpdateRequest, Logic


telegram_app = FastAPI()


@telegram_app.post("/webhook")
@inject
async def webhook(
    request: Request,
    telegram_webhook: TelegramWebhookService = Depends(Provide[Logic.services.webhook_telegram]),
):
    print('test')
    data = await request.json()
    res = telegram_webhook.process_update(TelegramUpdateRequest(**data))
    return {"message": "Hello World from main app"}