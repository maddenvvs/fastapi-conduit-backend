from typing import Any, Callable

import pytest
from typing_extensions import TypeAlias

from conduit.domain.users.email_address import EmailAddress

EmailAddressFactory: TypeAlias = Callable[[str], EmailAddress]


@pytest.fixture
def email_address_factory() -> EmailAddressFactory:
    def factory(value: str) -> EmailAddress:
        return EmailAddress(value)

    return factory


@pytest.fixture(
    params=[
        "a@b.com",
        "admin@google.com",
        "user@domain.org",
    ],
)
def valid_email_value(request: pytest.FixtureRequest) -> Any:
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
def invalid_email_type_value(request: pytest.FixtureRequest) -> Any:
    return request.param


@pytest.fixture(
    params=[
        "",
        "@",
        "www.site.com",
        "@domain.net",
        "user@.co.uk",
    ],
)
def invalid_email_value(request: pytest.FixtureRequest) -> Any:
    return request.param


@pytest.fixture
def valid_email_address(
    valid_email_value: str,
    email_address_factory: EmailAddressFactory,
) -> EmailAddress:
    return email_address_factory(valid_email_value)


def test_email_equals_to_itself(valid_email_address: EmailAddress) -> None:
    assert valid_email_address == valid_email_address  # noqa: PLR0124


def test_email_equals_to_str(
    valid_email_address: EmailAddress,
    valid_email_value: str,
) -> None:
    assert valid_email_address == valid_email_value


def test_email_not_equal_to_wrong_str(
    valid_email_address: EmailAddress,
    valid_email_value: str,
) -> None:
    assert valid_email_address != f"invalid_{valid_email_value}"


def test_email_equals_to_created_email_with_same_str(
    valid_email_address: EmailAddress,
    valid_email_value: str,
    email_address_factory: EmailAddressFactory,
) -> None:
    assert valid_email_address == email_address_factory(valid_email_value)


def test_email_not_equal_to_created_email_with_different_str(
    valid_email_address: EmailAddress,
    email_address_factory: EmailAddressFactory,
) -> None:
    assert valid_email_address != email_address_factory("fake@address.com")


def test_email_cannot_be_non_str(
    email_address_factory: EmailAddressFactory,
    invalid_email_type_value: Any,
) -> None:
    with pytest.raises(ValueError, match="Invalid email type"):
        email_address_factory(invalid_email_type_value)


def test_email_cannot_have_invalid_format(
    email_address_factory: EmailAddressFactory,
    invalid_email_value: str,
) -> None:
    with pytest.raises(ValueError, match="Invalid email format"):
        email_address_factory(invalid_email_value)
