import pytest
from httpx import AsyncClient, Request, codes


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("method", "url"),
    [
        ("GET", "/user"),
        ("PUT", "/user"),
    ],
)
async def test_visiting_protected_endpoints_returns_unauthorized_response(
    method: str,
    url: str,
    test_base_url: str,
    anonymous_test_client: AsyncClient,
) -> None:
    # Arrange
    request = Request(
        method=method,
        url=test_base_url + url,
    )

    # Act
    response = await anonymous_test_client.send(request)

    # Assert
    assert response.status_code == codes.UNAUTHORIZED
    assert response.json() == {"detail": "Missing authorization credentials"}
