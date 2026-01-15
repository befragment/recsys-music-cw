from typing import List
from domain.entity.track import Track
from domain.entity.interaction import InteractionAction


class RecommendationModel:
    def pick_next(
        self, interaction: InteractionAction, liked: List[Track], disliked: List[Track]
    ) -> Track:
        # TODO: Implement recommendation logic
        return
