import pytest
from httpx import AsyncClient, Request


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("method", "url"),
    [
        ("GET", "/user"),
        ("PUT", "/user"),
        ("POST", "/profiles/some-profile/follow"),
        ("DELETE", "/profiles/some-profile/follow"),
        ("GET", "/articles/feed"),
        ("POST", "/articles"),
        ("PUT", "/articles/some-slug"),
        ("DELETE", "/articles/some-slug"),
        ("POST", "/articles/some-slug/comments"),
        ("DELETE", "/articles/some-slug/comments/123"),
        ("POST", "/articles/some-slug/favorite"),
        ("DELETE", "/articles/some-slug/favorite"),
    ],
)
async def test_visiting_protected_endpoints_returns_unauthorized_response(
    method: str,
    url: str,
    test_base_url: str,
    any_client: AsyncClient,
) -> None:
    # Arrange
    request = Request(
        method=method,
        url=test_base_url + url,
    )

    # Act
    response = await any_client.send(request)

    # Assert
    assert response.status_code == 401
    assert response.json() == {"detail": "Missing authorization credentials."}
