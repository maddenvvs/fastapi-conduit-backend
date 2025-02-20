from typing import final

from dependency_injector import containers, providers

from conduit.domain.services.auth_token_service import AuthTokenService
from conduit.domain.services.password_service import PasswordService
from conduit.domain.services.profiles_service import ProfilesService
from conduit.domain.services.slug_service import SlugService
from conduit.domain.services.tags_service import TagsService
from conduit.domain.use_cases.create_article.use_case import CreateArticleUseCase
from conduit.domain.use_cases.get_article_by_slug.use_case import (
    GetArticleBySlugUseCase,
)
from conduit.domain.use_cases.get_current_user.use_case import GetCurrentUserUseCase
from conduit.domain.use_cases.get_profile_by_name.use_case import (
    GetProfileByNameUseCase,
)
from conduit.domain.use_cases.list_articles.use_case import ListArticlesUseCase
from conduit.domain.use_cases.list_tags.use_case import ListTagsUseCase
from conduit.domain.use_cases.login_user.use_case import LoginUserUseCase
from conduit.domain.use_cases.register_user.use_case import RegisterUserUseCase
from conduit.domain.use_cases.update_current_user.use_case import (
    UpdateCurrentUserUseCase,
)
from conduit.infrastructure.persistence.database import Database
from conduit.infrastructure.persistence.repositories.articles import (
    SQLiteArticlesRepository,
)
from conduit.infrastructure.persistence.repositories.followers import (
    SQLiteFollowersRepository,
)
from conduit.infrastructure.persistence.repositories.tags import SQLiteTagsRepository
from conduit.infrastructure.persistence.repositories.users import SQLiteUsersRepository
from conduit.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWorkFactory
from conduit.infrastructure.time import current_time
from conduit.settings import get_settings


@final
class Container(containers.DeclarativeContainer):

    __self__: providers.Self["Container"] = providers.Self()

    wiring_config = containers.WiringConfiguration(packages=[".api"])

    app_settings = providers.Singleton(get_settings)

    db = providers.Singleton(
        Database,
        db_url=app_settings.provided.database_url,
    )

    uow_factory = providers.Factory(
        SqlAlchemyUnitOfWorkFactory,
        db=db,
    )

    now = providers.Object(current_time)

    slug_service = providers.Singleton(SlugService)

    password_service = providers.Singleton(PasswordService)

    # Repositories

    tags_repository = providers.Factory(
        SQLiteTagsRepository,
        now=now,
    )

    users_repository = providers.Factory(
        SQLiteUsersRepository,
        now=now,
    )

    followers_repository = providers.Factory(
        SQLiteFollowersRepository,
        now=now,
    )

    articles_repository = providers.Factory(
        SQLiteArticlesRepository,
        now=now,
    )

    # Services

    tags_service = providers.Factory(
        TagsService,
        tags_repository=tags_repository,
    )

    auth_token_service = providers.Factory(
        AuthTokenService,
        secret_key=app_settings.provided.jwt_secret_key,
        algorithm=app_settings.provided.jwt_algorithm,
        token_expiration_minutes=app_settings.provided.jwt_token_expiration_minutes,
    )

    profiles_service = providers.Factory(
        ProfilesService,
        users_repository=users_repository,
        followers_repository=followers_repository,
    )

    # Use cases

    register_user_use_case = providers.Factory(
        RegisterUserUseCase,
        uow_factory=uow_factory,
        users_repository=users_repository,
        auth_token_service=auth_token_service,
        password_hasher=password_service.provided.hash_password,
    )

    login_user_use_case = providers.Factory(
        LoginUserUseCase,
        uow_factory=uow_factory,
        users_repository=users_repository,
        password_checker=password_service.provided.check_password,
        auth_token_service=auth_token_service,
        now=now,
    )

    list_tags_use_case = providers.Factory(
        ListTagsUseCase,
        uow_factory=uow_factory,
        tags_service=tags_service,
    )

    get_article_by_slug_use_case = providers.Factory(
        GetArticleBySlugUseCase,
    )

    create_article_use_case = providers.Factory(
        CreateArticleUseCase,
        uow_factory=uow_factory,
        profiles_service=profiles_service,
        slug_service=slug_service,
        tags_repository=tags_repository,
        articles_repository=articles_repository,
    )

    list_articles_use_case = providers.Factory(
        ListArticlesUseCase,
        uow_factory=uow_factory,
        articles_repository=articles_repository,
    )

    get_current_user_use_case = providers.Factory(
        GetCurrentUserUseCase,
    )

    update_current_user_use_case = providers.Factory(
        UpdateCurrentUserUseCase,
        uow_factory=uow_factory,
        users_repository=users_repository,
        password_hasher=password_service.provided.hash_password,
    )

    get_profile_by_name_use_case = providers.Factory(
        GetProfileByNameUseCase,
        uow_factory=uow_factory,
        profiles_service=profiles_service,
    )
