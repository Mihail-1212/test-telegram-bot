from aiogram import types


def create_poll_kb() -> types.ReplyKeyboardMarkup:
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(
        text="Создать опрос",
        request_poll=types.KeyboardButtonPollType(type=types.PollType.REGULAR),
    ))

    poll_keyboard.add(types.KeyboardButton(text="Отмена"))

    return poll_keyboard


def create_share_chat_kb() -> types.ReplyKeyboardMarkup:
    chat_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    chat_keyboard.add(types.InlineKeyboardButton(
        text="Выбрать чат",
        request_chat=types.KeyboardButtonRequestChat(request_id=1, chat_is_channel=False)
    ))

    chat_keyboard.add(types.KeyboardButton(text="Отмена"))

    return chat_keyboard


def remove_poll_kb() -> types.ReplyKeyboardRemove:
    remove_keyboard = types.ReplyKeyboardRemove()
    return remove_keyboard
