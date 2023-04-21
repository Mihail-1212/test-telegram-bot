import logging
from typing import Any

from aiogram import Dispatcher, types
from aiogram.utils.exceptions import InvalidHTTPUrlContent

from telebot.commands import get_bot_command_manager
from telebot.services import Service


logger = logging.getLogger()


async def cmd_random_animal(msg: types.Message, services: Service) -> Any:
    """
    Handler for /randomanimal command
    :param services:
    :param msg:types.Message
    """
    random_image: str = ""
    try:
        random_image = await services.random_animal_service.get_random_animal_image_url()
        return await msg.bot.send_photo(msg.chat.id, random_image)
    except InvalidHTTPUrlContent as _exc:
        """
        If random picture is not available fot telegram
        """
        logger.warning(f"{random_image} url is not available")
        return await cmd_random_animal(msg, services)
    except Exception as _exc:
        logger.error(f"{random_image} url make error!", extra={
            "error": str(_exc)
        })
        await msg.answer(text="Произошла неизвестная ошибка!")


def register_random_animal_handler(dp: Dispatcher) -> None:
    bot_command_manager = get_bot_command_manager()
    get_random_animal_cmd = bot_command_manager.random_animal_cmd.command

    dp.register_message_handler(cmd_random_animal, commands=[get_random_animal_cmd])
