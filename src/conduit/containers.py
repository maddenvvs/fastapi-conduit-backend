from typing import final

from dependency_injector import containers, providers

from conduit.api.settings import get_settings
from conduit.domain.services.articles import ArticlesService
from conduit.domain.services.tags import TagsService
from conduit.domain.services.users.user_auth_service import UserAuthService
from conduit.persistence.database import Database
from conduit.persistence.repositories.articles import InMemoryArticlesRepository
from conduit.persistence.unit_of_work import SqliteUnitOfWork


@final
class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=[".api.endpoints"])

    app_settings = providers.Singleton(get_settings)

    db = providers.Singleton(
        Database,
        db_url=app_settings.provided.database_url,
    )

    unit_of_work = providers.Factory(
        SqliteUnitOfWork,
        db=db,
    )

    tags_service = providers.Factory(
        TagsService,
        unit_of_work=unit_of_work,
    )

    articles_repository = providers.Factory(
        InMemoryArticlesRepository,
    )

    articles_service = providers.Factory(
        ArticlesService,
        repository=articles_repository,
    )

    user_auth_service = providers.Factory(
        UserAuthService,
    )
