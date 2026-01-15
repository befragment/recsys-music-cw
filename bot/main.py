import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config import settings
from core.start import start
from core.container import Container
from core.middleware import ContainerMiddleware


async def main():
    """Главная функция запуска бота"""

    # Создаем DI контейнер
    container = Container()
    container.config.from_dict(settings.model_dump())

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # Регистрируем middleware для инъекции контейнера
    dp.message.middleware(ContainerMiddleware(container))
    dp.callback_query.middleware(ContainerMiddleware(container))

    await start(dp, bot)


if __name__ == "__main__":
    asyncio.run(main())
