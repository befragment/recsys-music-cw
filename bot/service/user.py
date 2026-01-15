from typing import List

from domain.entity.user import User, InteractionAction
from domain.entity.track import Track
from service._contract import UserRepositoryProtocol, RecommendationModelProtocol, TrackRepositoryProtocol


class UserService:
    def __init__(
        self, 
        model: RecommendationModelProtocol,
        user_repository: UserRepositoryProtocol,
        track_repository: TrackRepositoryProtocol,
    ):
        self.model = model
        self.user_repository = user_repository
        self.track_repository = track_repository

    async def create(self, user: User) -> User:
        return await self.user_repository.create(user)

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return await self.user_repository.get_by_telegram_id(telegram_id)

    async def get_liked_tracks(self, user_id: int) -> List[Track]:
        return await self.user_repository.get_liked_tracks(user_id)

    async def get_disliked_tracks(self, user_id: int) -> List[Track]:
        return await self.user_repository.get_disliked_tracks(user_id)

    async def handle_user_interaction(
        self, telegram_id: int, track_id: int, interaction_type: InteractionAction
    ) -> Track:
        user_id = await self.user_repository.get_user_id_by_telegram_id(
            telegram_id
        )

        if user_id is None:
            raise ValueError(f"User with telegram_id {telegram_id} not found")

        await self.user_repository.create_interaction(
            user_id=user_id,
            track_id=track_id,
            action=interaction_type,
        )

        user_likes: List[Track] = await self.user_repository.get_liked_tracks(user_id)

        next_track_path: str = self.model.pick_next(
            user_likes
        )

        next_track: Track = await self.track_repository.get_track_by_path(next_track_path)

        return next_track
