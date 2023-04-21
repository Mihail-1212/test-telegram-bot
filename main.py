import asyncio
import logging
import os
from distutils.util import strtobool
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import (
    TELEBOT_API_TOKEN,
    POLLING_SKIP_UPDATES_KEY,
    WEATHER_API_TOKEN,
    CURRENCY_CONVERSION_API_TOKEN,
)
from telebot import handlers, services as telebot_services, startup_handler
from telebot.middleware import ServiceMiddleware


# Configure logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()


def register_handlers(dp: Dispatcher) -> None:
    """
    Register all handlers
    :param dp:
    :return:
    """
    handlers.register_start_handlers(dp)
    handlers.register_weather_handlers(dp)
    handlers.register_currency_conversion_handlers(dp)
    handlers.register_random_animal_handler(dp)
    handlers.register_create_send_polls_handlers(dp)


def register_middlewares(dp: Dispatcher, services: telebot_services.Service) -> None:
    """
    Register all middlewares to dispatcher
    :param dp:
    :param services:
    :return:
    """
    dp.middleware.setup(ServiceMiddleware(services))


def create_services() -> telebot_services.Service:
    """
    Create Service object instance to use in handlers
    :return: {Service} object instance
    """
    weather_api_key = os.getenv(WEATHER_API_TOKEN)
    convert_currency_api_key = os.getenv(CURRENCY_CONVERSION_API_TOKEN)

    services = telebot_services.Service(
        weather_service=telebot_services.WeatherService(weather_api_key=weather_api_key),
        currency_conversion_service=telebot_services.CurrencyConversionService(
            convert_currency_api_key=convert_currency_api_key
        ),
        random_animal_service=telebot_services.RandomAnimalService(),
        create_polls_service=telebot_services.CreatePollsService()
    )
    return services


async def main() -> None:
    # Load env variables from .env file
    load_dotenv()

    telebot_api_token = os.getenv(TELEBOT_API_TOKEN)
    polling_skip_updates = strtobool(os.getenv(POLLING_SKIP_UPDATES_KEY, "False"))

    storage = MemoryStorage()

    bot = Bot(token=telebot_api_token)
    dp = Dispatcher(bot, storage=storage)

    # TODO: api token check
    services = create_services()

    register_middlewares(dp, services)
    register_handlers(dp)

    try:
        if polling_skip_updates:
            # Skip updates
            await dp.skip_updates()

        # Startup func
        await startup_handler(dp)

        # Start polling
        await dp.start_polling()
    except Exception as _exc:
        logger.exception(msg="Error on dispatcher polling")


if __name__ == "__main__":
    asyncio.run(main())
