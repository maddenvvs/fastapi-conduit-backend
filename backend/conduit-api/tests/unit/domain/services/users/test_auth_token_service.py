import datetime
import logging
from typing import Any
from unittest import mock

import pytest

from conduit.domain.entities.users import User
from conduit.domain.services.auth_token_service import (
    AuthTokenService,
    IncorrectJwtTokenError,
)


@pytest.fixture
def auth_token_service_logger() -> Any:
    return mock.create_autospec(spec=logging.Logger, spec_set=True)


@pytest.fixture
def auth_token_service(auth_token_service_logger: logging.Logger) -> AuthTokenService:
    return AuthTokenService(
        secret_key="very_long_secret_key_to_use_for_test",  # noqa: S106
        algorithm="HS256",
        token_expiration_minutes=30,
        logger=auth_token_service_logger,
    )


def test_parse_valid_token_produces_correct_token_payload(
    auth_token_service: AuthTokenService,
) -> None:
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiSm9obiBEb2UifQ.gvogduV7_BTMZH7LZ-c7atu1bUKEdHc743ggO3N_Bmc"  # noqa: S105

    token_data = auth_token_service.parse_jwt_token(token)

    assert token_data.user_id == 123


class TestParseInvalidToken:
    @pytest.fixture(
        params=[
            "invalid.token.value",
            "",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzIiwidXNlcm5hbWUiOiJKb2huIERvZSJ9.ZXjZuq_OM3VOYhLbjbpgldlBsTnyGQdgHvshyokLmH",
        ],
    )
    def invalid_token(self, request: pytest.FixtureRequest) -> Any:
        return request.param

    def test_parse_token_raises_exception(
        self,
        auth_token_service: AuthTokenService,
        invalid_token: str,
    ) -> None:
        with pytest.raises(IncorrectJwtTokenError):
            auth_token_service.parse_jwt_token(invalid_token)

    def test_parse_token_logs_error_message(
        self,
        auth_token_service: AuthTokenService,
        auth_token_service_logger: mock.Mock,
    ) -> None:
        invalid_token = "invalid.token.value"  # noqa: S105

        with pytest.raises(IncorrectJwtTokenError):
            auth_token_service.parse_jwt_token(invalid_token)

        auth_token_service_logger.exception.assert_called_once_with(
            "Invalid JWT token",
            extra={
                "token": invalid_token,
                "error": mock.ANY,
            },
        )


def test_generate_token_produces_non_empty_token(
    auth_token_service: AuthTokenService,
) -> None:
    user = User(
        id=321,
        username="Magnus Carlsen",
        email="a@a.com",
        bio="",
        image=None,
        password_hash="",
    )
    current_time = datetime.datetime(
        2000,
        1,
        1,
        0,
        0,
        0,
        0,
        tzinfo=datetime.timezone.utc,
    )

    token_data = auth_token_service.generate_jwt_token(
        user=user,
        current_time=current_time,
    )

    assert len(token_data) > 0
