from typing import Dict, Callable, List

from contracts import InteractionRepositoryProtocol
from domain.entity.track import Track
from domain.entity.interaction import Interaction
from domain.entity.interaction import InteractionAction

class InteractionService:
    def __init__(
        self,
        interaction_repository: InteractionRepositoryProtocol,
        user_repository: UserRepositoryProtocol,
        recsys_model: RecommendationModelProtocol
    ):
        self.interaction_repository = interaction_repository
        self.user_repository = user_repository
        self.model = recsys_model

        # self.__handlers: Dict[InteractionAction, Callable[None, Track | None]] = {
        #     InteractionAction.skip: self.__handle_skip,
        #     InteractionAction.like: self.__handle_like,
        #     InteractionAction.dislike: self.__handle_dislike,
        # }

    async def handle_user_interaction(
        self, 
        telegram_id: int, 
        track_id: int, 
        interaction_type: InteractionAction
    ) -> Track:
        interaction = await self.interaction_repository.create(Interaction(
            user_id=user_id,
            track_id=track_id,
            action=interaction_type,
        )) # сохраняем `взаимодейтсвие` в бд

        user_id: int = await self.user_repository.get_user_id_by_telegram_id(telegram_id)

        user_likes: List[Track] = await self.user_repository.get_liked_tracks(user_id)
        user_dislikes: List[Track] = await self.user_repository.get_disliked_tracks(user_id)

        next_track: Track = await self.model.predict_next(
            interaction_type,
            user_likes, 
            user_dislikes
        )

        return next_track