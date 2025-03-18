import uuid
from collections.abc import AsyncGenerator, Generator
from datetime import datetime, timezone
from typing import Any, Callable, Protocol

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from typing_extensions import AsyncContextManager, TypeAlias

from conduit.app import create_app
from conduit.containers import Container
from conduit.infrastructure.persistence.database_seeder import Database
from conduit.infrastructure.persistence.models import Base, UserModel
from conduit.infrastructure.persistence.models import Base as ModelBase
from conduit.settings import Settings

ApiClientFactory: TypeAlias = Callable[[], AsyncClient]
UserModelFactory: TypeAlias = Callable[..., UserModel]
TokenFactory: TypeAlias = Callable[[UserModel], str]


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
    with container.app_settings.override(test_settings):  # type: ignore
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
async def generate_token(test_container: Container) -> TokenFactory:
    def factory(user_model: UserModel) -> str:
        auth_token_service = test_container.auth_token_service()
        return auth_token_service.generate_jwt_token(user_model.to_user())

    return factory


@pytest.fixture
async def registered_user_token(
    registered_user: UserModel,
    generate_token: TokenFactory,
) -> str:
    return generate_token(registered_user)


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
        },
        {
            "user_id": uuid.UUID("55555555666666667777777788888888"),
            "username": "admin_user",
        },
    ],
)
async def any_client(
    request: pytest.FixtureRequest,
    user_model_factory: UserModelFactory,
    test_client_factory: ApiClientFactory,
    add_to_db: AddToDb,
    generate_token: TokenFactory,
) -> AsyncGenerator[AsyncClient, None]:
    user_credentials = request.param
    if user_credentials is None:
        async with test_client_factory() as client:
            yield client
    else:
        user = user_model_factory(
            user_id=user_credentials["user_id"],
            username=user_credentials["username"],
        )
        await add_to_db(user)
        token = generate_token(user)
        async with test_client_factory() as client:
            client.headers["Authorization"] = f"Token {token}"
            yield client
