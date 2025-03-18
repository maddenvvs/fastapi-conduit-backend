from collections.abc import AsyncGenerator
from typing import Any, Callable

import pytest
from httpx import AsyncClient, Response, codes
from sqlalchemy import delete
from typing_extensions import TypeAlias

from conduit.infrastructure.common.persistence.models import UserModel
from conduit.shared.infrastructure.persistence.database import Database

RegisterRequest: TypeAlias = dict[str, Any]
RequestFactory: TypeAlias = Callable[..., RegisterRequest]


@pytest.fixture
def register_request_factory() -> RequestFactory:
    def factory(**kwargs: Any) -> dict[str, Any]:
        default_values = {
            "username": "walkmansit",
            "email": "walkmansit@gmail.com",
            "password": "1qazxsw23edc",
        }
        return {
            "user": {
                **default_values,
                **kwargs,
            },
        }

    return factory


class TestWhenRegisteringWithInvalidRequestFields:
    @pytest.fixture(
        params=[
            {"username": ""},
            {"password": ""},
            {"email": ""},
            {"email": "@.cm"},
        ],
    )
    def invalid_register_request(
        self,
        request: pytest.FixtureRequest,
        register_request_factory: RequestFactory,
    ) -> RegisterRequest:
        return register_request_factory(**request.param)

    @pytest.fixture
    async def register_response(
        self,
        any_client: AsyncClient,
        invalid_register_request: RegisterRequest,
    ) -> Response:
        return await any_client.post("/users", json=invalid_register_request)

    @pytest.mark.anyio
    async def test_returns_status_422(self, register_response: Response) -> None:
        assert register_response.status_code == codes.UNPROCESSABLE_ENTITY

    @pytest.mark.anyio
    async def test_has_body_with_erros(self, register_response: Response) -> None:
        r = register_response.json()

        assert "errors" in r
        assert len(r["errors"]) > 0


class TestWhenRegisteredSuccessully:
    @pytest.fixture(
        params=[
            {"username": "ivan", "password": "clear", "email": "a@a.com"},
            {"username": "ivan", "password": "very_strong_one", "email": "a@aabc.com"},
            {
                "username": "gobyna",
                "password": "uncertain",
                "email": "booking@aabc.com",
            },
        ],
    )
    async def request_body(
        self,
        register_request_factory: RequestFactory,
        request: pytest.FixtureRequest,
    ) -> RegisterRequest:
        return register_request_factory(**request.param)

    @pytest.fixture
    async def successful_response(
        self,
        request_body: RegisterRequest,
        any_client: AsyncClient,
        test_db: Database,
    ) -> AsyncGenerator[Response, None]:
        response = await any_client.post(
            "/users",
            json=request_body,
        )

        yield response

        async with test_db.create_session() as session:
            await session.execute(
                delete(UserModel).where(
                    UserModel.email == request_body["user"]["email"],
                ),
            )
            await session.commit()

    @pytest.mark.anyio
    async def test_returns_status_201(self, successful_response: Response) -> None:
        assert successful_response.status_code == codes.CREATED

    @pytest.mark.anyio
    async def test_returns_body_with_created_user_details(
        self,
        successful_response: Response,
        request_body: RegisterRequest,
    ) -> None:
        r = successful_response.json()

        assert len(r["user"]) == 5  # noqa: PLR2004
        assert r["user"]["email"] == request_body["user"]["email"]
        assert r["user"]["username"] == request_body["user"]["username"]
        assert r["user"]["bio"] == ""
        assert r["user"]["image"] is None
        assert len(r["user"]["token"]) > 0


class TestWhenUsernameIsTaken:
    @pytest.fixture
    async def failed_response(
        self,
        registered_user: UserModel,
        any_client: AsyncClient,
        register_request_factory: RequestFactory,
    ) -> Response:
        request = register_request_factory(username=registered_user.username)
        return await any_client.post("/users", json=request)

    @pytest.mark.anyio
    async def test_returns_error_status(self, failed_response: Response) -> None:
        assert failed_response.status_code == codes.BAD_REQUEST

    @pytest.mark.anyio
    async def test_returns_body_with_clarification(
        self,
        failed_response: Response,
    ) -> None:
        assert failed_response.json() == {
            "detail": "Username is already in use",
        }


class TestWhenEmailIsTaken:
    @pytest.fixture
    async def failed_response(
        self,
        registered_user: UserModel,
        any_client: AsyncClient,
        register_request_factory: RequestFactory,
    ) -> Response:
        request = register_request_factory(email=registered_user.email)
        return await any_client.post("/users", json=request)

    @pytest.mark.anyio
    async def test_returns_error_status(self, failed_response: Response) -> None:
        assert failed_response.status_code == codes.BAD_REQUEST

    @pytest.mark.anyio
    async def test_returns_body_with_clarification(
        self,
        failed_response: Response,
    ) -> None:
        assert failed_response.json() == {
            "detail": "Email is already in use",
        }
