from typing import List

from domain.entity.user import User
from domain.entity.track import Track
from service._contract import UserRepositoryProtocol


class UserService:
    def __init__(self, user_repository: UserRepositoryProtocol):
        self.user_repository = user_repository

    async def create(self, user: User) -> User:
        return await self.user_repository.create(user)

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return await self.user_repository.get_by_telegram_id(telegram_id)

    async def get_liked_tracks(self, user_id: int) -> List[Track]:
        return await self.user_repository.get_liked_tracks(user_id)

    async def get_disliked_tracks(self, user_id: int) -> List[Track]:
        return await self.user_repository.get_disliked_tracks(user_id)
