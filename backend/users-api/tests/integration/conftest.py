import uuid
from collections.abc import AsyncGenerator, Generator
from datetime import datetime, timezone
from typing import Any, Callable, Protocol
from unittest import mock

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from typing_extensions import AsyncContextManager, TypeAlias

from conduit.app import create_app
from conduit.containers import Container
from conduit.infrastructure.common.persistence.models import Base, UserModel
from conduit.infrastructure.common.persistence.models import Base as ModelBase
from conduit.settings import Settings
from conduit.shared.infrastructure.messaging.rabbitmq_broker import RabbitMQBroker
from conduit.shared.infrastructure.persistence.database import Database

ApiClientFactory: TypeAlias = Callable[[], AsyncClient]
UserModelFactory: TypeAlias = Callable[..., UserModel]


class AddToDb(Protocol):
    async def __call__(self, *args: Base) -> None: ...


class DatabaseContext(Protocol):
    def __call__(self, *entities: Base) -> AsyncContextManager[None]: ...


@pytest.fixture(scope="session")
def test_base_url() -> str:
    return "http://testserver/api"


@pytest.fixture(scope="session")
def test_sqlite_database_url(tmp_path_factory: pytest.TempPathFactory) -> str:
    database_path = tmp_path_factory.mktemp("test_sqlite_database") / "test.db"
    return f"sqlite+aiosqlite:///{database_path.absolute()}"


@pytest.fixture(scope="session")
def test_settings(
    test_sqlite_database_url: str,
) -> Settings:
    return Settings.model_validate(
        {
            "database_url": test_sqlite_database_url,
            "debug": True,
            "jwt_secret_key": "secret_key_example_for_test_purposes",
            "jwt_token_expiration_minutes": 60 * 24,
        },
    )


@pytest.fixture(scope="session")
def test_container(test_settings: Any) -> Generator[Container, None, None]:
    container = Container()
    with (
        container.app_settings.override(test_settings),  # type: ignore
        container.message_broker.override(mock.create_autospec(spec=RabbitMQBroker)),  # type: ignore
    ):
        yield container


@pytest.fixture(scope="session")
def test_app(test_container: Container) -> FastAPI:
    return create_app(test_container)


@pytest.fixture
def test_client_factory(test_app: FastAPI, test_base_url: str) -> ApiClientFactory:
    def factory() -> AsyncClient:
        return AsyncClient(
            transport=ASGITransport(app=test_app),
            base_url=test_base_url,
            headers={
                "Content-Type": "application/json",
            },
        )

    return factory


@pytest.fixture(scope="session")
def test_db(test_container: Container) -> Database:
    return test_container.db()


@pytest.fixture(scope="session", autouse=True)
async def create_db_tables(
    test_db: Database,
) -> AsyncGenerator[None, None]:
    await test_db.create_tables(ModelBase)
    yield
    await test_db.drop_tables(ModelBase)


@pytest.fixture
async def add_to_db(
    test_db: Database,
) -> AsyncGenerator[AddToDb, None]:
    entities: list[Base] = []

    async def _add_to_db(*args: Base) -> None:
        for entity in args:
            entities.append(entity)
            session.add(entity)
        await session.commit()

    async with test_db.create_session() as session:
        yield _add_to_db
        for entity in entities:
            await session.delete(entity)
        await session.commit()


@pytest.fixture
async def user_model_factory() -> UserModelFactory:
    def factory(**kwargs: Any) -> UserModel:
        default_kwagrs: dict[str, Any] = {
            "user_id": uuid.UUID("12345678123456781234567812345678"),
            "username": "admin",
            "email": "admin@gmail.com",
            "password_hash": "oops_i_did_it_again",
            "bio": "Admin user.",
            "image_url": None,
            "created_at": datetime(year=2020, month=1, day=1, tzinfo=timezone.utc),
            "updated_at": datetime(year=2020, month=1, day=1, tzinfo=timezone.utc),
        }
        user_model_args = {**default_kwagrs, **kwargs}
        return UserModel(**user_model_args)

    return factory


@pytest.fixture
async def registered_user(
    user_model_factory: UserModelFactory,
    add_to_db: AddToDb,
) -> UserModel:
    user_model = user_model_factory()
    await add_to_db(user_model)
    return user_model


@pytest.fixture
async def registered_user_token(
    test_client_factory: ApiClientFactory,
    registered_user: UserModel,
) -> Any:
    async with test_client_factory() as client:
        login_response = await client.post(
            "/users/login",
            json={
                "user": {
                    "email": registered_user.email,
                    "password": registered_user.password_hash,
                },
            },
        )
    return login_response.json()["user"]["token"]


@pytest.fixture
async def registered_user_client(
    test_client_factory: ApiClientFactory,
    registered_user_token: str,
) -> AsyncGenerator[AsyncClient, None]:
    async with test_client_factory() as client:
        client.headers["Authorization"] = f"Token {registered_user_token}"
        yield client


@pytest.fixture
async def anonymous_test_client(
    test_client_factory: ApiClientFactory,
) -> AsyncGenerator[AsyncClient, None]:
    async with test_client_factory() as client:
        yield client


@pytest.fixture(
    params=[
        None,
        {
            "user_id": uuid.UUID("11111111222222223333333344444444"),
            "username": "test_user",
            "email": "test_user@testland.com",
            "password": "super_password",
        },
        {
            "user_id": uuid.UUID("55555555666666667777777788888888"),
            "username": "admin_user",
            "email": "admin_user@testland.com",
            "password": "wow_look_at_the_password",
        },
    ],
)
async def any_client(
    request: pytest.FixtureRequest,
    user_model_factory: UserModelFactory,
    test_client_factory: ApiClientFactory,
    add_to_db: AddToDb,
) -> AsyncGenerator[AsyncClient, None]:
    user_credentials = request.param
    if user_credentials is None:
        async with test_client_factory() as client:
            yield client
    else:
        user = user_model_factory(
            user_id=user_credentials["user_id"],
            username=user_credentials["username"],
            email=user_credentials["email"],
            password_hash=user_credentials["password"],
        )
        await add_to_db(user)
        async with test_client_factory() as client:
            response = await client.post(
                "/users/login",
                json={
                    "user": {
                        "email": user_credentials["email"],
                        "password": user_credentials["password"],
                    },
                },
            )
            token = response.json()["user"]["token"]
            client.headers["Authorization"] = f"Token {token}"
            yield client
