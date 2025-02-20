from typing import Any, AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from conduit.app import create_app
from conduit.containers import Container
from conduit.infrastructure.persistence.database import Database
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
