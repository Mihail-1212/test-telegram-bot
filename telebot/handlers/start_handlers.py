from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart

from telebot.commands.commands import get_bot_commands_menu_str

WELCOME_TEXT = """
Привет! Это тестовый телеграм бот.
Он может:
"""


async def cmd_start(msg: types.Message) -> None:
    """
    Handler for /start command
    :param msg:types.Message
    """
    welcome_text = WELCOME_TEXT

    commands_menu_str = get_bot_commands_menu_str()
    welcome_text += f"\n{commands_menu_str}"

    await msg.answer(
        text=welcome_text
    )


def register_start_handlers(dp: Dispatcher) -> None:

    dp.register_message_handler(cmd_start, commands=CommandStart().commands)
