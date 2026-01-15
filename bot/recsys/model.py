from typing import List
from domain.entity.track import Track
from domain.entity.interaction import InteractionAction
import pickle
import numpy as np

class RecommendationModel:
    def __init__(
            self, 
            tracks_ids: List[int],
            track_embeddings: np.ndarray
    ):
        with open("recommender_model.pkl", "rb") as f:
            self.model = pickle.load(f)
        self.track_ids = tracks_ids
        self.track_embeddings = track_embeddings
    
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
        if len(likes) == 0:
            return int(np.random.choice(self.track_ids))
        last_tracks = likes[-3:]
        embs = [t.embedding for t in last_tracks]
        user_emb = np.mean(embs, axis=0).reshape(1, -1)
        _ , indices = self.model.kneighbors(user_emb, n_neighbors=5)
        liked_ids = {t.id for t in likes}

        for idx in indices[0]:
            candidate_id = self.track_ids[idx]
            if candidate_id not in liked_ids:
                return candidate_id

        return self.track_ids[indices[0][0]]
    
    @staticmethod
    def __build_path(track_id: int) -> str:
        return f"/app/data/fma_small/{track_id:06d}/{track_id:06d}.mp3"
