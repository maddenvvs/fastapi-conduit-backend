from typing import final

from dependency_injector import containers, providers

from conduit.api.security.auth_token_service import AuthTokenService
from conduit.application.users.use_cases.get_current_user.use_case import (
    GetCurrentUserUseCase,
)
from conduit.application.users.use_cases.register_user.use_case import (
    RegisterUserUseCase,
)
from conduit.infrastructure.common.current_time import current_time
from conduit.infrastructure.common.persistence.database import Database
from conduit.infrastructure.common.persistence.unit_of_work import (
    SqlAlchemyUnitOfWorkFactory,
)
from conduit.infrastructure.users.repositories.users_repository import (
    SQLiteUsersRepository,
)
from conduit.infrastructure.users.services.password_service import PasswordService
from conduit.settings import get_settings


@final
class Container(containers.DeclarativeContainer):
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

    password_service = providers.Singleton(PasswordService)

    # Repositories

    users_repository = providers.Factory(
        SQLiteUsersRepository,
        now=now,
        password_hasher=password_service.provided.hash_password,
    )

    # Services

    auth_token_service = providers.Factory(
        AuthTokenService,
        secret_key=app_settings.provided.jwt_secret_key,
        algorithm=app_settings.provided.jwt_algorithm,
        token_expiration_minutes=app_settings.provided.jwt_token_expiration_minutes,
    )

    # Use cases

    get_current_user_use_case = providers.Factory(
        GetCurrentUserUseCase,
    )

    register_user_use_case = providers.Factory(
        RegisterUserUseCase,
        uow_factory=uow_factory,
        users_repository=users_repository,
    )
