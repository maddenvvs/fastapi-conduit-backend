import pytest
from httpx import AsyncClient, Response

from tests.integration.conftest import AddToDb, UserModelFactory


class TestWhenLoginWithEmptyPassword:
    @pytest.fixture
    async def login_response(self, any_client: AsyncClient) -> Response:
        response = await any_client.post(
            url="/users/login",
            json=dict(
                user=dict(
                    email="a@a.com",
                    password="",
                ),
            ),
        )
        return response

    @pytest.mark.anyio
    async def test_returns_status_422_invalid_request(
        self,
        login_response: Response,
    ) -> None:
        assert login_response.status_code == 422

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
        response = await any_client.post(
            url="/users/login",
            json=dict(
                user=dict(
                    email=request.param,
                    password="password",
                ),
            ),
        )
        return response

    @pytest.mark.anyio
    async def test_returns_status_422_invalid_request(
        self,
        login_response: Response,
    ) -> None:
        assert login_response.status_code == 422

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
            dict(email="a@a.com", password="123"),
            dict(email="bob@company.io", password="password"),
            dict(email="alice@jets.co.uk", password="!paswd!d2ds"),
        ],
    )
    async def login_response(
        self,
        request: pytest.FixtureRequest,
        any_client: AsyncClient,
    ) -> Response:
        param = request.param
        response = await any_client.post(
            url="/users/login",
            json=dict(
                user=dict(
                    email=param["email"],
                    password=param["password"],
                ),
            ),
        )
        return response

    @pytest.mark.anyio
    async def test_returns_status_401_unauthorized(
        self,
        login_response: Response,
    ) -> None:
        assert login_response.status_code == 401

    @pytest.mark.anyio
    async def test_returns_empty_response(self, login_response: Response) -> None:
        assert login_response.json() is None


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
            password_hash="very_strong_password",
        )
        await add_to_db(user)

    class TestWithValidCredentials:
        @pytest.fixture
        async def login_response(self, any_client: AsyncClient) -> Response:
            response = await any_client.post(
                url="/users/login",
                json=dict(
                    user=dict(
                        email="walkmansit@gmail.com",
                        password="very_strong_password",
                    ),
                ),
            )
            return response

        @pytest.mark.anyio
        async def test_returns_status_200_ok(self, login_response: Response) -> None:
            assert login_response.status_code == 200

        @pytest.mark.anyio
        async def test_returns_jwt_token(self, login_response: Response) -> None:
            json_response = login_response.json()

            assert len(json_response["user"]["token"]) > 0

    class TestWithInvalidPassword:
        @pytest.fixture
        async def login_response(self, any_client: AsyncClient) -> Response:
            response = await any_client.post(
                url="/users/login",
                json=dict(
                    user=dict(
                        email="walkmansit@gmail.com",
                        password="invalid_password",
                    ),
                ),
            )
            return response

        @pytest.mark.anyio
        async def test_returns_status_401_unauthorized(
            self,
            login_response: Response,
        ) -> None:
            assert login_response.status_code == 401

        @pytest.mark.anyio
        async def test_returns_empty_body(self, login_response: Response) -> None:
            assert login_response.json() is None
