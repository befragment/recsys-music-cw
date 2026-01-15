from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from core.container import Container
from domain.entity.user import User
from handler._keyboards import (
    create_empty_keyboard,
    create_gender_keyboard,
    create_genre_keyboard,
)

router = Router()


class Form(StatesGroup):
    gender = State()
    age = State()
    genre = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, container: Container):
    """Начало работы: проверяем пользователя и начинаем анкету"""
    # Получаем user_service для проверки
    user_service = container.user_service()

    # Проверяем, есть ли пользователь
    existing_user = await user_service.get_by_telegram_id(message.from_user.id)

    if existing_user:
        # Пользователь уже есть - показываем команды
        await message.answer(
            "С возвращением!\n\n"
            "Команды:\n"
            "/music - музыкальный плеер\n"
            "/liked - понравившиеся треки\n"
            "/disliked - непонравившиеся треки",
            reply_markup=create_empty_keyboard(),
        )
        return

    # Новый пользователь - начинаем анкету
    await state.clear()

    await message.answer(
        "Добро пожаловать в музыкального бота!\n"
        "Для рекомендаций пройдите небольшую анкету",
        reply_markup=create_empty_keyboard(),
    )

    await message.answer("Выберите ваш пол:", reply_markup=create_gender_keyboard())

    await state.set_state(Form.gender)


@router.callback_query(F.data.startswith("gender_"), Form.gender)
async def handle_gender(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    gender_map = {"gender_male": "мужской", "gender_female": "женский"}
    gender = gender_map.get(callback.data, "мужской")

    await state.update_data(gender=gender)
    await callback.message.edit_text(
        f"Пол: {gender.capitalize()}\n\nУкажите ваш возраст (от 10 до 100):"
    )

    await state.set_state(Form.age)


@router.message(Form.age)
async def handle_age(message: Message, state: FSMContext):
    try:
        age = int(message.text.strip())

        if age < 10 or age > 100:
            await message.answer("Введите возраст от 10 до 100 лет:")
            return

        await state.update_data(age=age)

        await message.answer(
            f"Возраст: {age} лет\n\nВыберите любимый жанр:",
            reply_markup=create_genre_keyboard(),
        )

        await state.set_state(Form.genre)

    except ValueError:
        await message.answer("Введите число:")


@router.callback_query(F.data.startswith("genre_"), Form.genre)
async def handle_genre(
    callback: CallbackQuery, state: FSMContext, container: Container
):
    await callback.answer()

    genre_map = {
        "genre_rock": "рок",
        "genre_pop": "поп",
        "genre_classical": "классика",
        "genre_electronic": "электроника",
        "genre_hiphop": "хип-хоп",
        "genre_jazz": "джаз",
        "genre_metal": "метал",
        "genre_mixed": "смешанный",
    }

    genre = genre_map.get(callback.data, "смешанный")
    user_data = await state.get_data()

    # Создаем пользователя через user_service
    try:
        user_service = container.user_service()

        # Создаем пользователя с данными анкеты
        user = User(
            telegram_id=callback.from_user.id,
            gender=user_data["gender"],
            age=user_data["age"],
            favorite_music_genre=genre,
        )

        created_user = await user_service.create(user)
        print(f"Пользователь создан: {created_user}")

    except Exception as e:
        print(f"Ошибка создания пользователя: {e}")
        # Продолжаем даже при ошибке

    await callback.message.edit_text(
        f"Анкета заполнена!\n\n"
        f"• Пол: {user_data['gender'].capitalize()}\n"
        f"• Возраст: {user_data['age']} лет\n"
        f"• Жанр: {genre.capitalize()}\n\n"
        f"Команды:\n"
        f"/music - музыкальный плеер\n"
        f"/liked - понравившиеся треки\n"
        f"/disliked - непонравившиеся треки"
    )

    await state.clear()
