from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from core.container import Container

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, container: Container):
    """Обработчик команды /start"""
    # Получаем сервис пользователей
    user_service = container.user_service()
    
    # Вызываем метод watafapepe
    await user_service.watafapepe()
    
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        "Я бот для рекомендации музыки. 🎵"
    )

