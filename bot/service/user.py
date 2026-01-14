from domain.entity.user import User
from contracts import UserRepositoryProtocol

class UserService:
    def __init__(self, user_repository: UserRepositoryProtocol):
        self.user_repository = user_repository

    def create(self, telegram_id: int) -> User:
        return await self.user_repository.create(User)

    def get_liked_tracks(self, user_id: int) -> list[Track]:
        return await self.user_repository.get_liked_tracks(user_id)

    def get_disliked_tracks(self, user_id: int) -> list[Track]:
        return await self.user_repository.get_disliked_tracks(user_id)
