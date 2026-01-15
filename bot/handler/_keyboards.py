from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_gender_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Мужской", callback_data="gender_male"),
        InlineKeyboardButton(text="Женский", callback_data="gender_female"),
    )
    builder.adjust(2)
    return builder.as_markup()


def create_genre_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    genres = [
        ("🎸 Рок", "genre_rock"),
        ("🎤 Поп", "genre_pop"),
        ("🎻 Классика", "genre_classical"),
        ("🎧 Электроника", "genre_electronic"),
        ("🎵 Хип-хоп", "genre_hiphop"),
        ("🎷 Джаз", "genre_jazz"),
        ("🤘 Метал", "genre_metal"),
        ("🌈 Смешанный", "genre_mixed"),
    ]
    for text, callback in genres:
        builder.button(text=text, callback_data=callback)
    builder.adjust(2)
    return builder.as_markup()


def create_player_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="❤️", callback_data="player:like"),
        InlineKeyboardButton(text="💔", callback_data="player:dislike"),
        InlineKeyboardButton(text="⏭️", callback_data="player:skip"),
    )
    builder.adjust(3)
    return builder.as_markup()


def create_empty_keyboard():
    return None  # или ReplyKeyboardRemove()
