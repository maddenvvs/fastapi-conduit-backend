from typing import final

from dependency_injector import containers, providers

from conduit.application.users.use_cases.get_current_user.use_case import (
    GetCurrentUserUseCase,
)
from conduit.application.users.use_cases.login_user.use_case import LoginUserUseCase
from conduit.application.users.use_cases.register_user.use_case import (
    RegisterUserUseCase,
)
from conduit.application.users.use_cases.update_current_user.use_case import (
    UpdateCurrentUserUseCase,
)
from conduit.infrastructure.users.messaging.events_publisher import (
    RabbitMQEventsPublisher,
)
from conduit.infrastructure.users.repositories.users_repository import (
    SQLiteUsersRepository,
)
from conduit.infrastructure.users.services.login_service import SQLiteLoginService
from conduit.infrastructure.users.services.password_service import PasswordService
from conduit.settings import get_settings
from conduit.shared.api.security.auth_token_service import AuthTokenService
from conduit.shared.infrastructure.current_time import current_time
from conduit.shared.infrastructure.messaging.rabbitmq_broker import RabbitMQBroker
from conduit.shared.infrastructure.persistence.database import Database
from conduit.shared.infrastructure.persistence.unit_of_work import (
    SqlAlchemyUnitOfWorkFactory,
)


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

    message_broker = providers.Singleton(
        RabbitMQBroker,
        rabbitmq_url=app_settings.provided.rabbitmq_url,
    )

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

    login_service = providers.Factory(
        SQLiteLoginService,
        password_hasher=password_service.provided.hash_password,
    )

    events_publisher = providers.Factory(
        RabbitMQEventsPublisher,
        broker=message_broker,
    )

    # Use cases

    get_current_user_use_case = providers.Factory(
        GetCurrentUserUseCase,
    )

    register_user_use_case = providers.Factory(
        RegisterUserUseCase,
        uow_factory=uow_factory,
        users_repository=users_repository,
        events_publisher=events_publisher,
    )

    update_current_user_use_case = providers.Factory(
        UpdateCurrentUserUseCase,
        uow_factory=uow_factory,
        users_repository=users_repository,
        events_publisher=events_publisher,
    )

    login_user_use_case = providers.Factory(
        LoginUserUseCase,
        uow_factory=uow_factory,
        login_service=login_service,
    )
