from typing import List
from domain.entity.track import Track
from domain.entity.interaction import InteractionAction


class RecommendationModel:
    def pick_next(
        self, 
        likes: List[Track], 
    ) -> str: 
        """
        Main method of model.
        """
        next_track_id = self.__predict(likes)
        return self.__build_path(next_track_id)

    def __predict(self, likes: List[Track]) -> int:
        """
        Pick next track to play based on user's interaction history and preferences.
        Args:
            likes: List[Track] - list of tracks the user liked (last 5)
        Returns:
            int - the ID of the next track to play (from dataset)
        """
        ...

    @staticmethod
    def __build_path(track_id: int) -> str:
        return f"/app/data/fma_small/{track_id:06d}/{track_id:06d}.mp3"
