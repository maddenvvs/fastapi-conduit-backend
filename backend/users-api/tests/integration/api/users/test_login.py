import pytest
from httpx import AsyncClient, Response, codes

from tests.integration.conftest import AddToDb, UserModelFactory


class TestWhenLoginWithEmptyPassword:
    @pytest.fixture
    async def login_response(self, any_client: AsyncClient) -> Response:
        return await any_client.post(
            url="/users/login",
            json={
                "user": {
                    "email": "a@a.com",
                    "password": "",
                },
            },
        )

    @pytest.mark.anyio
    async def test_returns_error_status(
        self,
        login_response: Response,
    ) -> None:
        assert login_response.status_code == codes.UNPROCESSABLE_ENTITY

    @pytest.mark.anyio
    async def test_returns_json_with_error_reason(
        self,
        login_response: Response,
    ) -> None:
        assert login_response.json() == {
            "errors": {"password": ["String should have at least 1 character"]},
        }


class TestWhenLoginWithInvalidEmail:
    @pytest.fixture(
        params=[
            "",
            "abc",
            "a.com",
            "@.com",
            "b@.com",
            "@asdasd.com",
        ],
    )
    async def login_response(
        self,
        request: pytest.FixtureRequest,
        any_client: AsyncClient,
    ) -> Response:
        return await any_client.post(
            url="/users/login",
            json={
                "user": {
                    "email": request.param,
                    "password": "password",
                },
            },
        )

    @pytest.mark.anyio
    async def test_returns_error_status(
        self,
        login_response: Response,
    ) -> None:
        assert login_response.status_code == codes.UNPROCESSABLE_ENTITY

    @pytest.mark.anyio
    async def test_returns_json_with_error_reason(
        self,
        login_response: Response,
    ) -> None:
        json_response = login_response.json()

        assert len(json_response) == 1
        assert len(json_response["errors"]) == 1
        assert len(json_response["errors"]["email"]) > 0


class TestWhenLoginToNonexistingUser:
    @pytest.fixture(
        params=[
            {"email": "a@a.com", "password": "123"},
            {"email": "bob@company.io", "password": "password"},
            {"email": "alice@jets.co.uk", "password": "!paswd!d2ds"},
        ],
    )
    async def login_response(
        self,
        request: pytest.FixtureRequest,
        any_client: AsyncClient,
    ) -> Response:
        param = request.param
        return await any_client.post(
            url="/users/login",
            json={
                "user": {
                    "email": param["email"],
                    "password": param["password"],
                },
            },
        )

    @pytest.mark.anyio
    async def test_returns_status_401_unauthorized(
        self,
        login_response: Response,
    ) -> None:
        assert login_response.status_code == codes.UNAUTHORIZED

    @pytest.mark.anyio
    async def test_returns_response_body(
        self,
        login_response: Response,
    ) -> None:
        assert login_response.json() == {"detail": "Unauthorized"}


class TestWhenLoginToExistingUser:
    @pytest.fixture(autouse=True)
    async def create_valid_user(
        self,
        user_model_factory: UserModelFactory,
        add_to_db: AddToDb,
    ) -> None:
        user = user_model_factory(
            username="walkmansit",
            email="walkmansit@gmail.com",
            password_hash="very_strong_password",  # noqa: S106
        )
        await add_to_db(user)

    class TestWithValidCredentials:
        @pytest.fixture
        async def login_response(self, any_client: AsyncClient) -> Response:
            return await any_client.post(
                url="/users/login",
                json={
                    "user": {
                        "email": "walkmansit@gmail.com",
                        "password": "very_strong_password",
                    },
                },
            )

        @pytest.mark.anyio
        async def test_returns_status_200_ok(self, login_response: Response) -> None:
            assert login_response.status_code == codes.OK

        @pytest.mark.anyio
        async def test_returns_jwt_token(self, login_response: Response) -> None:
            json_response = login_response.json()

            assert len(json_response["user"]["token"]) > 0

    class TestWithInvalidPassword:
        @pytest.fixture
        async def login_response(self, any_client: AsyncClient) -> Response:
            return await any_client.post(
                url="/users/login",
                json={
                    "user": {
                        "email": "walkmansit@gmail.com",
                        "password": "invalid_password",
                    },
                },
            )

        @pytest.mark.anyio
        async def test_returns_status_401_unauthorized(
            self,
            login_response: Response,
        ) -> None:
            assert login_response.status_code == codes.UNAUTHORIZED

        @pytest.mark.anyio
        async def test_returns_response_body(
            self,
            login_response: Response,
        ) -> None:
            assert login_response.json() == {"detail": "Unauthorized"}
