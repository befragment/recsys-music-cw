from typing import Protocol, List

from domain.entity.track import Track
from domain.entity.user import User, InteractionAction

"""
Файл в котором мы определяем контракты для работы с бизнес-логикой приложения.
Это позволяет нам использовать DI для работы с бизнес-логикой приложения.
"""


class UserServiceProtocol(Protocol):
    async def create(self, telegram_id: int) -> User: ...

    async def get_by_telegram_id(self, telegram_id: int) -> User | None: ...

    async def get_liked_tracks(self, user_id: int) -> List[Track]: ...

    async def get_disliked_tracks(self, user_id: int) -> List[Track]: ...

    async def handle_user_interaction(
        self, telegram_id: int, track_id: int, interaction_type: InteractionAction
    ) -> Track: ...


class TrackServiceProtocol(Protocol): 
    async def get_all_tracks(self) -> List[Track]: ...
    
    async def get_track_by_path(self, path: str) -> Track | None: ...
