from typing import List, Protocol
from domain.entity.track import Track
from domain.entity.interaction import InteractionType

"""
Файл в котором мы определяем контракты для работы с базой данных.
Это позволяет нам использовать DI для работы с базой данных.
"""

class TrackRepositoryProtocol(Protocol):
    ...

class UserRepositoryProtocol(Protocol):
    ...

class InteractionRepositoryProtocol(Protocol):
    ...

class RecommendationModelProtocol(Protocol):
    def pick_next(
        self, 
        interaction: InteractionAction, 
        liked: List[Track], 
        disliked: List[Track]
    ) -> Track: ... 