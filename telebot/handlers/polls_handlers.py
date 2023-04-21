from typing import Any

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from telebot.commands import get_bot_command_manager
from telebot.keyboards import (
    create_poll_kb,
    create_share_chat_kb,
    remove_poll_kb
)
from telebot.services import Service


class CreatePollState(StatesGroup):
    poll_id = State()
    chat_id = State()


async def cmd_create_polls(msg: types.Message, state: FSMContext, services: Service) -> Any:
    """
    Handler for /createpolls command
    Start CreatePollState processing and render new keyboard to create new poll
    """
    if msg.chat.type != types.ChatType.PRIVATE:
        return await msg.answer(text="Вы можете создавать опрос только в приватном чате!")

    # Set state
    await state.set_state(CreatePollState.poll_id.state)

    # Create poll keyboard
    poll_ikb = create_poll_kb()
    await msg.answer("Нажмите на кнопку ниже и создайте опрос! ", reply_markup=poll_ikb)


async def process_create_poll(msg: types.Message, state: FSMContext, services: Service) -> Any:
    """
    Handler for CreatePollState.poll_id state
    Create poll and render new keyboard to send new poll to chat
    """
    poll_id = services.create_polls_service.create_user_poll(
        poll_id=msg.poll.id,
        question=msg.poll.question,
        options=[o.text for o in msg.poll.options],
        owner_id=msg.from_user.id
    )
    await state.set_state(CreatePollState.chat_id.state)
    await state.update_data(poll_id=str(poll_id))

    # Create pick chat keyboard
    share_chat_kb = create_share_chat_kb()

    await msg.answer(text="Вы успешно создали опрос! Теперь отправьте его в чат!", reply_markup=share_chat_kb)


async def process_send_poll(msg: types.Message, state: FSMContext, services: Service) -> Any:
    """
    Handler for CreatePollState.chat_id state
    Send poll handler
    :param state:
    :param msg:
    :param services:
    :return:
    """
    async with state.proxy() as data:
        # Объект {ChatShared} имеет атрибут user_id вместо chat_id (как по документации Telegram),
        # поэтому достал chat_id как из словаря
        data["chat_id"] = msg.chat_shared['chat_id']

        # Getting new poll
        user_poll = services.create_polls_service.get_poll_by_id(poll_id=data["poll_id"])

        # Send poll to chat
        await msg.bot.send_poll(chat_id=data["chat_id"], question=user_poll.question, is_anonymous=False,
                                options=user_poll.options, type="regular")
        # Create new markup to remove keyboard
        remove_kb = remove_poll_kb()
        await msg.answer(text="Вы успешно отправили опрос в чат!", reply_markup=remove_kb)

    await state.finish()


async def cancel_create_send_poll(msg: types.Message, state: FSMContext, services: Service) -> Any:
    """
    Cancel process handler - cancel process and remove kb
    """
    await state.finish()
    remove_kb = remove_poll_kb()
    await msg.answer("Создание опроса отменено.", reply_markup=remove_kb)


def register_create_send_polls_handlers(dp: Dispatcher) -> None:
    bot_command_manager = get_bot_command_manager()
    create_send_poll_cmd = bot_command_manager.create_send_polls_cmd.command

    # Register commands
    dp.register_message_handler(cmd_create_polls, commands=[create_send_poll_cmd])

    # Register state handlers
    dp.register_message_handler(process_create_poll, content_types=[types.ContentType.POLL],
                                state=CreatePollState.poll_id)
    dp.register_message_handler(process_send_poll, content_types=[types.ContentType.CHAT_SHARED],
                                state=CreatePollState.chat_id)

    # Register cancel handler on all states of CreatePollState
    dp.register_message_handler(
        cancel_create_send_poll,
        lambda message: message.text == "Отмена",
        state=CreatePollState.all_states
    )
