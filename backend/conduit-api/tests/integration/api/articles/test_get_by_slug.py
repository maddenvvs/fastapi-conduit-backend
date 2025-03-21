import datetime
from typing import Any

import pytest
from httpx import AsyncClient, Response, codes

from conduit.infrastructure.persistence.models import ArticleModel, UserModel
from tests.integration.conftest import UserModelFactory


class TestWhenThereIsNoArticleWithGivenTag:
    @pytest.fixture
    async def get_article_response(self, any_client: AsyncClient) -> Response:
        return await any_client.get("/articles/non-existing-article")

    @pytest.mark.anyio
    async def test_returns_404_not_found(self, get_article_response: Response) -> None:
        assert get_article_response.status_code == codes.NOT_FOUND

    @pytest.mark.anyio
    async def test_returns_json_with_message(
        self,
        get_article_response: Response,
    ) -> None:
        assert get_article_response.json() == {"detail": "Article not found"}


class TestWhenArticleExists:
    @pytest.fixture
    def article_author(self, user_model_factory: UserModelFactory) -> UserModel:
        return user_model_factory(
            username="article_author",
        )

    @pytest.fixture(autouse=True)
    async def setup_article(
        self,
        article_author: UserModel,
        add_to_db: Any,
    ) -> None:
        await add_to_db(article_author)
        article = ArticleModel(
            author_id=article_author.id,
            slug="article-slug",
            title="Article Title",
            description="Article description",
            body="Article body",
            created_at=datetime.datetime(
                year=2021,
                month=11,
                day=26,
                tzinfo=datetime.timezone.utc,
            ),
            updated_at=datetime.datetime(
                year=2022,
                month=12,
                day=1,
                tzinfo=datetime.timezone.utc,
            ),
        )
        await add_to_db(article)

    @pytest.fixture
    async def get_article_response(
        self,
        any_client: AsyncClient,
    ) -> Response:
        return await any_client.get("/articles/article-slug")

    @pytest.mark.anyio
    async def test_returns_200_ok(self, get_article_response: Response) -> None:
        assert get_article_response.status_code == codes.OK

    @pytest.mark.anyio
    async def test_returns_json_with_article_data(
        self,
        get_article_response: Response,
        article_author: UserModel,
    ) -> None:
        assert get_article_response.json() == {
            "article": {
                "slug": "article-slug",
                "title": "Article Title",
                "description": "Article description",
                "body": "Article body",
                "tagList": [],
                "createdAt": "2021-11-26T00:00:00Z",
                "updatedAt": "2022-12-01T00:00:00Z",
                "favorited": False,
                "favoritesCount": 0,
                "author": {
                    "username": article_author.username,
                    "bio": article_author.bio,
                    "image": article_author.image_url,
                    "following": False,
                },
            },
        }
