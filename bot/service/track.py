from typing import List

from service._contract import TrackRepositoryProtocol
from domain.entity.track import Track


class TrackService:
    def __init__(self, track_repository: TrackRepositoryProtocol):
        self.track_repository = track_repository

    async def get_all_tracks(self) -> List[Track]:
        return await self.track_repository.get_all_tracks()


