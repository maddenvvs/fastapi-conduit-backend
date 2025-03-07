from typing import Any, Callable

import pytest
from typing_extensions import TypeAlias

from conduit.domain.users.username import Username

UsernameFactory: TypeAlias = Callable[[str], Username]


@pytest.fixture
def username_factory() -> UsernameFactory:
    def factory(username: str) -> Username:
        return Username(username)

    return factory


@pytest.fixture(
    params=[
        "user",
        "admin",
        "ochen_horosho",
        "two words",
        "😎",
        "русский_богатырь",
    ],
)
def valid_username_value(request: pytest.FixtureRequest) -> Any:
    return request.param


@pytest.fixture(
    params=[
        0,
        -1,
        24,
        3.14,
        True,
        1 + 2j,
        lambda: (),
        object(),
    ],
)
def invalid_username_value(request: pytest.FixtureRequest) -> Any:
    return request.param


@pytest.fixture(
    params=[
        "",
        "a" * 21,
        "very_long_username_with_specific_meaning",
    ],
)
def username_with_invalid_length(request: pytest.FixtureRequest) -> Any:
    return request.param


@pytest.fixture
def valid_username(
    valid_username_value: str,
    username_factory: UsernameFactory,
) -> Username:
    return username_factory(valid_username_value)


def test_username_equals_to_itself(valid_username: Username) -> None:
    assert valid_username == valid_username  # noqa: PLR0124


def test_username_equals_to_str(
    valid_username: Username,
    valid_username_value: str,
) -> None:
    assert valid_username == valid_username_value


def test_username_not_equal_to_wrong_str(
    valid_username: Username,
    valid_username_value: str,
) -> None:
    assert valid_username != f"invalid_{valid_username_value}"


def test_username_equals_to_created_username_with_same_str(
    valid_username: Username,
    valid_username_value: str,
    username_factory: UsernameFactory,
) -> None:
    assert valid_username == username_factory(valid_username_value)


def test_username_not_equal_to_created_username_with_different_str(
    valid_username: Username,
    username_factory: UsernameFactory,
) -> None:
    assert valid_username != username_factory("different_username")


def test_username_cannot_be_non_str(
    username_factory: UsernameFactory,
    invalid_username_value: Any,
) -> None:
    with pytest.raises(ValueError, match="Invalid username"):
        username_factory(invalid_username_value)


def test_username_must_satisfy_length_requirements(
    username_factory: UsernameFactory,
    username_with_invalid_length: str,
) -> None:
    with pytest.raises(ValueError, match="Username length must be between"):
        username_factory(username_with_invalid_length)
