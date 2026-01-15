from typing import List, Protocol

from domain.entity.track import Track
from domain.entity.user import User
from domain.entity.interaction import Interaction, InteractionAction

"""
Файл в котором мы определяем контракты для работы с базой данных.
Это позволяет нам использовать DI для работы с базой данных.
"""


class TrackRepositoryProtocol(Protocol):
    async def get_all_tracks(self) -> List[Track]: ...


class UserRepositoryProtocol(Protocol):
    async def create(self, user: User): ...

    async def get_by_telegram_id(self, telegram_id: int) -> User | None: ...

    async def get_user_id_by_telegram_id(self, telegram_id: int) -> int | None: ...

    async def get_telegram_id_by_user_id(self, user_id: int) -> int | None: ...

    async def get_user_tracks(self, user_id: int) -> List[Track]: ...

    async def get_liked_tracks(self, user_id: int) -> List[Track]: ...

    async def get_disliked_tracks(self, user_id: int) -> List[Track]: ...


class InteractionRepositoryProtocol(Protocol):
    async def create(self, interaction: Interaction): ...


class RecommendationModelProtocol(Protocol):
    def pick_next(
        self, interaction: InteractionAction, liked: List[Track], disliked: List[Track]
    ) -> Track: ...
