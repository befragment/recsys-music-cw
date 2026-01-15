from typing import List
import random
from domain.entity.track import Track


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
        return random.choice([2, 5, 10, 140, 141, 148, 182, 190, 193, 194, 197, 200, 203, 204, 207, 210, 211, 212, 213, 255, 256, 368, 424, 459, 534, 540, 546, 574, 602])

    @staticmethod
    def __build_path(track_id: int) -> str:
        return f"/app/data/fma_small/{track_id:06d}/{track_id:06d}.mp3"

    
