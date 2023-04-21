from typing import List

from aiogram import Dispatcher
from aiogram.types import BotCommand

from telebot.commands import get_bot_commands_menu


async def startup_handler(dp: Dispatcher) -> None:
    """
    Handler on start polling
    :param dp:
    :return:
    """
    bot_commands: List[BotCommand] = get_bot_commands_menu()
    await dp.bot.set_my_commands(bot_commands)
