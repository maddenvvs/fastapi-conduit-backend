from datetime import datetime
from typing import Any, AsyncGenerator, Callable

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

from conduit.app import create_app
from conduit.containers import Container
from conduit.infrastructure.persistence.database import Database
from conduit.infrastructure.persistence.models import UserModel
from conduit.settings import Settings


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
    settings = Settings(
        _env_file=None,  # type: ignore
        database_url=test_sqlite_database_url,
        debug=True,
        jwt_secret_key="secret_key_example_for_test_purposes",
        jwt_token_expiration_minutes=60 * 24,
    )
    return settings


@pytest.fixture(scope="session")
def test_app(test_settings: Settings) -> FastAPI:
    return create_app()


@pytest.fixture(scope="session")
def test_container(test_app: FastAPI) -> Any:
    return test_app.extra["container"]


@pytest.fixture(scope="session")
def test_db(test_container: Container) -> Database:
    return test_container.db()


@pytest.fixture(scope="session", autouse=True)
async def test_sqlite_database(
    test_db: Database,
) -> AsyncGenerator[None, None]:
    await test_db.create_tables()
    yield
    await test_db.drop_tables()


@pytest.fixture
async def anonymous_test_client(
    test_app: FastAPI,
    test_base_url: str,
) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=test_app),
        base_url=test_base_url,
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture(scope="session")
async def user_model_factory() -> Callable[..., UserModel]:
    def factory(**kwargs: Any) -> UserModel:
        default_kwagrs: dict[str, Any] = dict(
            username="admin",
            email="admin@gmail.com",
            password_hash="oops_i_did_it_again",
            bio="Admin user.",
            image_url=None,
            created_at=datetime(year=2020, month=1, day=1),
            updated_at=datetime(year=2020, month=1, day=1),
        )
        user_model_args = {**default_kwagrs, **kwargs}
        return UserModel(**user_model_args)

    return factory


@pytest.fixture(scope="session")
async def registered_user(user_model_factory: Callable[..., UserModel]) -> UserModel:
    return user_model_factory()


@pytest.fixture(scope="session", autouse=True)
async def create_test_users(
    test_sqlite_database: None,
    test_db: Database,
    registered_user: UserModel,
) -> AsyncGenerator[None, None]:
    async with test_db.create_session() as session:
        session.add(registered_user)
        await session.commit()
        yield
        await session.execute(delete(UserModel))
        await session.commit()


@pytest.fixture
async def registered_user_token(
    anonymous_test_client: AsyncClient,
    registered_user: UserModel,
) -> Any:
    response = await anonymous_test_client.post(
        "/users/login",
        json=dict(
            user=dict(
                email=registered_user.email,
                password=registered_user.password_hash,
            )
        ),
    )
    return response.json()["user"]["token"]


@pytest.fixture
async def registered_user_client(
    test_app: FastAPI,
    test_base_url: str,
    registered_user_token: str,
) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=test_app),
        base_url=test_base_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Token {registered_user_token}",
        },
    ) as client:
        yield client


@pytest.fixture(
    params=[
        None,
        dict(email="admin@gmail.com", password="oops_i_did_it_again"),
    ]
)
async def any_client(
    request: pytest.FixtureRequest,
    test_app: FastAPI,
    test_base_url: str,
) -> AsyncGenerator[AsyncClient, None]:
    user_credentials = request.param

    async with AsyncClient(
        transport=ASGITransport(app=test_app),
        base_url=test_base_url,
        headers={
            "Content-Type": "application/json",
        },
    ) as client:
        if user_credentials is not None:
            response = await client.post(
                "/users/login",
                json=dict(
                    user=dict(
                        email=user_credentials["email"],
                        password=user_credentials["password"],
                    )
                ),
            )
            token = response.json()["user"]["token"]
            client.headers["Authorization"] = f"Token {token}"

        yield client
