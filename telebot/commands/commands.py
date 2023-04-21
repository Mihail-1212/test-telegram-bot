from dataclasses import dataclass, fields
from typing import List

from aiogram.types import BotCommand

START_CMD = "start"
WEATHER_CMD = "weather"
CURRENCY_CONVERSION_CMD = "currencyconversion"
RANDOM_ANIMAL_CMD = "randomanimal"
CREATE_SEND_POLLS_CMD = "createsendpolls"

WEATHER_DESCRIPTION = "Определить текущую погоду в определенном городе"
CURRENCY_CONVERSION_DESCRIPTION = "Конвертировать валюты"
RANDOM_ANIMAL_DESCRIPTION = "Отправлять случайную картинку с милыми животными"
CREATE_SEND_POLLS_CMD_DESCRIPTION = "Создавать опросы с определенным вопросом и вариантами ответов и отправлять их в чат"


@dataclass
class BotCommandManager:
    """
    Data class contain all custom bot commands
    """
    weather_cmd = BotCommand(command=WEATHER_CMD, description=WEATHER_DESCRIPTION)
    currency_conversion_cmd = BotCommand(command=CURRENCY_CONVERSION_CMD, description=CURRENCY_CONVERSION_DESCRIPTION)
    random_animal_cmd = BotCommand(command=RANDOM_ANIMAL_CMD, description=RANDOM_ANIMAL_DESCRIPTION)
    create_send_polls_cmd = BotCommand(command=CREATE_SEND_POLLS_CMD, description=CREATE_SEND_POLLS_CMD_DESCRIPTION)

    def get_list_commands(self) -> List[BotCommand]:
        return [
            self.weather_cmd,
            self.currency_conversion_cmd,
            self.random_animal_cmd,
            self.create_send_polls_cmd
        ]


# Create instance of command manager
bot_command_manager = BotCommandManager()


def get_bot_command_manager() -> BotCommandManager:
    """
    Return BotManager instance to use in application
    :return:
    """
    global bot_command_manager
    return bot_command_manager


def get_bot_commands_menu() -> List[BotCommand]:
    """
    Return bot commands for user menu
    :return:
    """
    global bot_command_manager
    return bot_command_manager.get_list_commands()


def get_bot_commands_menu_str() -> str:
    """
    Return bot commands for user menu as string
    For example:
    /{command_1} - {Description_1}
    /{command_2} - {Description_2}
    """
    bot_commands_list = get_bot_commands_menu()
    result: str = ""
    for bot_command in bot_commands_list:
        result += f"/{bot_command.command} - {bot_command.description}\n"

    return result
