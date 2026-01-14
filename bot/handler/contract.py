from typing import Protocol, List

class InteractionServiceProtocol(Protocol):
    async def handle_user_interaction(
        self, 
        telegram_id: int, 
        track_id: int, 
        interaction_type: InteractionAction
    ) -> Track: 
        ...

class UserServiceProtocol(Protocol):
    async def create(self, telegram_id: int) -> User: ... 

    async def get_liked_tracks(self, user_id: int) -> List[Track]: ...

    async def get_disliked_tracks(self, user_id: int) -> List[Track]: ...


class TrackServiceProtocol(Protocol): ...