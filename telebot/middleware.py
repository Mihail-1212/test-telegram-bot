from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from telebot.services import Service


class ServiceMiddleware(BaseMiddleware):
    """
    Telegram dispatcher service middleware
    Register services instance for all handlers
    """

    def __init__(self, services: Service):
        self.services: Service = services
        super().__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        data["services"] = self.services
