from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from telebot.commands import get_bot_command_manager
from telebot.services.currency_conversion_service import CurrencyBadRequestError, CurrencyUnknownError
from telebot.services import Service


EXAMPLE_CURRENCY_CODE_URL = "http://www.consultant.ru/document/cons_doc_LAW_31966" \
                            "/5ebb56e60f3126b262bd44c2e7d258fea7179649/"


class CurrencyConversionState(StatesGroup):
    amount = State()
    from_code = State()
    to_code = State()


async def cmd_currency_conversion(msg: types.Message, services: Service) -> None:
    """
    Handler for /currencyconversion command
    :param services: telebot.services.services.Service
    :param msg:types.Message
    """
    # services.weather_service.get_weather_by_city("")
    # Set state
    await CurrencyConversionState.amount.set()

    await msg.answer(
        text="Для перевода курса валюты введите: сумму (через точку):"
    )


async def process_amount_invalid(message: types.Message, state: FSMContext, services: Service):
    """
    Handler for CurrencyConversionState.amount state if amount is invalid
    """
    return await message.reply("Сумма должна быть только числом!")


async def process_amount(message: types.Message, state: FSMContext, services: Service):
    """
    Handler for CurrencyConversionState.amount state if amount is valid
    """
    await CurrencyConversionState.next()
    await state.update_data(amount=float(message.text))

    await message.answer(f"Введите код валюты из которой вы хотите перевести")


async def process_from_code(message: types.Message, state: FSMContext, services: Service):
    """
    Handler for CurrencyConversionState.from_code state
    """
    async with state.proxy() as data:
        data['from_code'] = message.text

    await CurrencyConversionState.next()

    await message.answer(f"Введите код валюты в которую вы хотите перевести")


async def process_to_code(msg: types.Message, state: FSMContext, services: Service):
    """
    Handler for CurrencyConversionState.to_code state
    Finish currency conversion process and return result of conversion
    """
    async with state.proxy() as data:
        data['to_code'] = msg.text

        try:
            result = services.currency_conversion_service.convert_currency(data['amount'], data['from_code'], data['to_code'])
            await msg.answer(f"Ваш результат: {result} {data['to_code']}")
        except CurrencyBadRequestError as _exc:
            await msg.answer(text=f"Вы ввели неправильный код валюты или неправильную сумму! Попробуйте еще раз.\n"
                                  f"Код валюты вы можете найти на сайте {EXAMPLE_CURRENCY_CODE_URL}")
        except CurrencyUnknownError as _exc:
            await msg.answer(text=f"На сервере произошла неизвестная ошибка! "
                                  f"Код валюты вы можете найти на сайте {EXAMPLE_CURRENCY_CODE_URL}")

    # Finish conversation
    await state.finish()


def register_currency_conversion_handlers(dp: Dispatcher) -> None:
    bot_command_manager = get_bot_command_manager()
    currency_conversion_cmd = bot_command_manager.currency_conversion_cmd.command

    # Register command handler
    dp.register_message_handler(cmd_currency_conversion, commands=[currency_conversion_cmd])

    # Register process handlers
    dp.register_message_handler(process_amount_invalid,
                                lambda message: not message.text.replace(".", "", 1).isdigit(),
                                state=CurrencyConversionState.amount)
    dp.register_message_handler(process_amount,
                                lambda message: message.text.replace(".", "", 1).isdigit(),
                                state=CurrencyConversionState.amount)

    dp.register_message_handler(process_from_code, state=CurrencyConversionState.from_code)
    dp.register_message_handler(process_to_code, state=CurrencyConversionState.to_code)
