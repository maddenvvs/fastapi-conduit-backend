from typing import final

from dependency_injector import containers, providers

from conduit.api.settings import get_settings
from conduit.domain.services.articles import ArticlesService
from conduit.domain.services.tags import TagsService
from conduit.domain.services.users.auth_token_service import AuthTokenService
from conduit.domain.services.users.password_service import PasswordService
from conduit.domain.use_cases.list_tags.use_case import ListTagsUseCase
from conduit.domain.use_cases.login_user.use_case import LoginUserUseCase
from conduit.domain.use_cases.register_user.use_case import RegisterUserUseCase
from conduit.infrastructure.persistence.database import Database
from conduit.infrastructure.persistence.repositories.articles import (
    InMemoryArticlesRepository,
)
from conduit.infrastructure.persistence.unit_of_work import (
    SqliteUnitOfWork,
    context_factory,
)
from conduit.infrastructure.time import current_time


@final
class Container(containers.DeclarativeContainer):

    __self__: providers.Self["Container"] = providers.Self()

    wiring_config = containers.WiringConfiguration(packages=[".api.endpoints"])

    now = providers.Object(current_time)

    password_service = providers.Singleton(PasswordService)

    app_settings = providers.Singleton(get_settings)

    db = providers.Singleton(
        Database,
        db_url=app_settings.provided.database_url,
    )

    uow_context_factory = providers.Callable(
        context_factory,
        now=now,
    )

    unit_of_work = providers.Factory(
        SqliteUnitOfWork,
        db=db,
        context_factory=uow_context_factory,
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

    auth_token_service = providers.Factory(
        AuthTokenService,
        secret_key="secret_key",
        algorithm="HS256",
        token_expiration_minutes=30,
    )

    register_user_use_case = providers.Factory(
        RegisterUserUseCase,
        unit_of_work=unit_of_work,
        auth_token_service=auth_token_service,
        password_hasher=password_service.provided.hash_password,
    )

    login_user_use_case = providers.Factory(
        LoginUserUseCase,
        unit_of_work=unit_of_work,
        auth_token_service=auth_token_service,
        password_checker=password_service.provided.check_password,
        now=now,
    )

    list_tags_use_case = providers.Factory(
        ListTagsUseCase,
        tags_service=tags_service,
    )
