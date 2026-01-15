from aiogram import Dispatcher, Bot
from loguru import logger

from core.database import database_shutdown
from handler import start_router, audioplayer_router


def setup_handlers(dp: Dispatcher) -> None:
    """Регистрация всех обработчиков"""
    dp.include_router(start_router)
    dp.include_router(audioplayer_router)
    logger.info("Handlers registered successfully")


async def on_startup(bot: Bot) -> None:
    """Действия при запуске бота"""
    logger.info("Bot is starting...")
    bot_info = await bot.get_me()
    logger.info(f"Bot @{bot_info.username} started successfully")


async def on_shutdown(bot: Bot) -> None:
    """Действия при остановке бота"""
    logger.info("Bot is shutting down...")
    await database_shutdown()
    await bot.session.close()


async def start(dp: Dispatcher, bot: Bot) -> None:
    """Запуск бота с подключением обработчиков"""
    # Регистрация обработчиков
    setup_handlers(dp)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Запуск polling
    logger.info("Starting polling...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
