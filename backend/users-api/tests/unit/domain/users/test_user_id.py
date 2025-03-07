from typing import Any, Final, Optional, Protocol

import pytest

from conduit.domain.users.user_id import UserId


class UserIdFactory(Protocol):
    def __call__(self, id_: Optional[int] = None) -> UserId: ...


DEFAULT_USER_ID: Final = 1


@pytest.fixture
def user_id_factory() -> UserIdFactory:
    def factory(id_: Optional[int] = None) -> UserId:
        return UserId(DEFAULT_USER_ID if id_ is None else id_)

    return factory


@pytest.fixture(
    params=[
        10,
        22,
        444,
        31337,
        -904175,
    ],
)
def valid_id_value(request: pytest.FixtureRequest) -> Any:
    return request.param


@pytest.fixture(
    params=[
        "",
        "0",
        "4",
        "-1",
        "asdas",
        3.14,
        True,
        lambda: (),
        object(),
    ],
)
def invalid_id_value(request: pytest.FixtureRequest) -> Any:
    return request.param


@pytest.fixture
def user_id(valid_id_value: int, user_id_factory: UserIdFactory) -> UserId:
    return user_id_factory(valid_id_value)


def test_user_id_equals_to_itself(user_id: UserId) -> None:
    assert user_id == user_id  # noqa: PLR0124


def test_user_id_equals_to_int_id(user_id: UserId, valid_id_value: int) -> None:
    assert user_id == valid_id_value


def test_user_id_not_equal_to_wrong_int(user_id: UserId, valid_id_value: int) -> None:
    assert user_id != (valid_id_value + 1)


def test_user_id_equals_to_created_user_id_with_same_int(
    user_id: UserId,
    valid_id_value: int,
    user_id_factory: UserIdFactory,
) -> None:
    assert user_id == user_id_factory(valid_id_value)


def test_user_id_not_equal_to_created_user_id_with_different_int(
    user_id: UserId,
    valid_id_value: int,
    user_id_factory: UserIdFactory,
) -> None:
    assert user_id != user_id_factory(valid_id_value + 1)


def test_user_id_cannot_be_non_integer(
    user_id_factory: UserIdFactory,
    invalid_id_value: Any,
) -> None:
    with pytest.raises(ValueError, match="Invalid user id"):
        user_id_factory(invalid_id_value)
