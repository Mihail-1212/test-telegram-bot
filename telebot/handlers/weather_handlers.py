import logging
from typing import Any

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from telebot.commands.commands import get_bot_command_manager
from telebot.services.services import Service
from telebot.services.weather_service import CityNotFoundError, WeatherApiUnauthorizedError

logger = logging.getLogger()


class WeatherState(StatesGroup):
    city_name = State()


async def cmd_weather(msg: types.Message, services: Service) -> None:
    """
    Handler for /weather command
    :param services: telebot.services.services.Service
    :param msg:types.Message
    """
    # Set state
    await WeatherState.city_name.set()

    await msg.answer(
        text="Для определения текущей погоды введите название города."
    )


async def process_city_weather(message: types.Message, state: FSMContext, services: Service) -> Any:
    """
    Handler for WeatherState.city_name state
    Process city name and return error or weather in this city
    :param message:
    :param state:
    :param services:
    """
    city_name = message.text
    # Stop asking for city name
    await state.finish()
    try:
        current_weather: BaseWeather = services.weather_service.get_weather_by_city(city_name)
    except CityNotFoundError as _exc:
        logger.info(f"City {city_name} was not found")
        return await message.answer(text="Город с таким названием не был найден, повторите попытку.")
    except WeatherApiUnauthorizedError as _exc:
        # If token is invalid
        logger.error("Weather token is invalid")
        return await message.answer(text="Ошибка на сервере! Обратитесь к системному администратору!")

    answer_message = f"""
Погода в указанном месте такова: 
{current_weather.detailed_status}, 
ветер со скоростью {str(current_weather.wind()['speed'])} м/с,
Температура: {str(current_weather.temperature('celsius')['temp'])} градусов по Цельсию
Облачность: {str(current_weather.clouds)}%
"""

    await message.answer(
        text= answer_message,
    )


def register_weather_handlers(dp: Dispatcher) -> None:
    bot_command_manager = get_bot_command_manager()
    get_weather_cmd = bot_command_manager.weather_cmd.command

    dp.register_message_handler(cmd_weather, commands=[get_weather_cmd])
    dp.register_message_handler(process_city_weather, state=WeatherState.city_name)
