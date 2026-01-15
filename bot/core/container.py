from dependency_injector import containers, providers

from core.database import async_session_factory
from repository.user import UserRepository
from repository.interaction import InteractionRepository
from repository.track import TrackRepository
from service.user import UserService
from service.interaction import InteractionService
from service.track import TrackService
from recsys.model import RecommendationModel


class Container(containers.DeclarativeContainer):
    """Главный DI контейнер приложения"""

    # Конфигурация
    config = providers.Configuration()

    # Database
    session_factory = providers.Factory(async_session_factory)

    # Repositories (создаются для каждого запроса)
    user_repository = providers.Factory(
        UserRepository,
        session=session_factory,
    )

    interaction_repository = providers.Factory(
        InteractionRepository,
        session=session_factory,
    )

    track_repository = providers.Factory(
        TrackRepository,
        session=session_factory,
    )

    # Model (singleton)
    recsys_model = providers.Singleton(
        RecommendationModel,
    )

    # Services (создаются для каждого запроса)
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    track_service = providers.Factory(
        TrackService,
        track_repository=track_repository,
    )

    interaction_service = providers.Factory(
        InteractionService,
        interaction_repository=interaction_repository,
        user_repository=user_repository,
        recsys_model=recsys_model,
    )
