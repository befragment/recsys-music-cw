from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ContainerMiddleware(BaseMiddleware):
    """Middleware для инъекции DI контейнера в обработчики"""
    
    def __init__(self, container):
        super().__init__()
        self.container = container
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Добавляем контейнер в данные
        data["container"] = self.container
        return await handler(event, data)

