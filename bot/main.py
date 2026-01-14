import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config import settings
from core.start import start


async def main():
    """Главная функция запуска бота"""
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML  # бот рендерит html
        )
    )
    dp = Dispatcher()
    
    await start(dp, bot)


if __name__ == "__main__":
    asyncio.run(main())
