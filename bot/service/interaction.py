from typing import List

from service._contract import (
    InteractionRepositoryProtocol,
    UserRepositoryProtocol,
    TrackRepositoryProtocol,
    RecommendationModelProtocol,
)
from domain.entity.track import Track
from domain.entity.interaction import Interaction
from domain.entity.interaction import InteractionAction


class InteractionService:
    def __init__(
        self,
        interaction_repository: InteractionRepositoryProtocol,
        user_repository: UserRepositoryProtocol,
        track_repository: TrackRepositoryProtocol,
        recsys_model: RecommendationModelProtocol,
    ):
        self.interaction_repository = interaction_repository
        self.user_repository = user_repository
        self.track_repository = track_repository
        self.model = recsys_model

    async def handle_user_interaction(
        self, telegram_id: int, track_id: int, interaction_type: InteractionAction
    ) -> Track:
        user_id = await self.user_repository.get_user_id_by_telegram_id(
            telegram_id
        )

        if user_id is None:
            raise ValueError(f"User with telegram_id {telegram_id} not found")

        await self.interaction_repository.create(
            Interaction(
                user_id=user_id,
                track_id=track_id,
                action=interaction_type,
            )
        )  # сохраняем `взаимодейтсвие` в бд

        user_likes: List[Track] = await self.user_repository.get_liked_tracks(user_id)

        next_track_path: str = self.model.pick_next(
            user_likes
        )

        next_track: Track = await self.track_repository.get_track_by_path(next_track_path)

        return next_track
