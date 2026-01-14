from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        "Я бот для рекомендации музыки. 🎵"
    )

