import datetime
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, Response
from sqlalchemy import delete

from conduit.infrastructure.persistence.database import Database
from conduit.infrastructure.persistence.models import ArticleModel


class TestWhenThereIsNoArticleWithGivenTag:

    class TestWhenVisitAnonymously:

        @pytest.fixture
        async def get_article_response(
            self,
            anonymous_test_client: AsyncClient,
        ) -> Response:
            response = await anonymous_test_client.get("/articles/non-existing-article")
            return response

        @pytest.mark.anyio
        async def test_returns_404_not_found(
            self, get_article_response: Response
        ) -> None:
            assert get_article_response.status_code == 404

        @pytest.mark.anyio
        async def test_returns_json_with_message(
            self, get_article_response: Response
        ) -> None:
            assert get_article_response.json() == {"detail": "Article not found"}

    class TestWhenVisitByRegisteredUser:

        @pytest.fixture
        async def get_article_response(
            self,
            registered_user_client: AsyncClient,
        ) -> Response:
            response = await registered_user_client.get(
                "/articles/non-existing-article"
            )
            return response

        @pytest.mark.anyio
        async def test_returns_404_not_found(
            self, get_article_response: Response
        ) -> None:
            assert get_article_response.status_code == 404

        @pytest.mark.anyio
        async def test_returns_json_with_message(
            self, get_article_response: Response
        ) -> None:
            assert get_article_response.json() == {"detail": "Article not found"}


class TestWhenArticleExists:

    @pytest.fixture(autouse=True)
    async def setup_article(self, test_db: Database) -> AsyncGenerator[None, None]:
        async with test_db.create_session() as session:
            article = ArticleModel(
                author_id=1,
                slug="article-slug",
                title="Article Title",
                description="Article description",
                body="Article body",
                created_at=datetime.datetime(year=2021, month=11, day=26),
                updated_at=datetime.datetime(year=2022, month=12, day=1),
            )

            session.add(article)
            await session.commit()
            yield

            await session.execute(delete(ArticleModel))
            await session.commit()

    class TestWhenVisitByRegisteredUser:

        @pytest.fixture
        async def get_article_response(
            self,
            registered_user_client: AsyncClient,
        ) -> Response:
            response = await registered_user_client.get("/articles/article-slug")
            return response

        @pytest.mark.anyio
        async def test_returns_200_OK(self, get_article_response: Response) -> None:
            assert get_article_response.status_code == 200

        @pytest.mark.anyio
        async def test_returns_json_with_article_data(
            self, get_article_response: Response
        ) -> None:
            assert get_article_response.json() == {
                "article": {
                    "slug": "article-slug",
                    "title": "Article Title",
                    "description": "Article description",
                    "body": "Article description",
                    "tagList": [],
                    "createdAt": "2021-11-26T00:00:00Z",
                    "updatedAt": "2022-12-01T00:00:00Z",
                    "favorited": False,
                    "favoritesCount": 0,
                    "author": {
                        "username": "admin",
                        "bio": "Admin user.",
                        "image": None,
                        "following": False,
                    },
                }
            }

    class TestWhenVisitAnonymously:

        @pytest.fixture
        async def get_article_response(
            self,
            anonymous_test_client: AsyncClient,
        ) -> Response:
            response = await anonymous_test_client.get("/articles/article-slug")
            return response

        @pytest.mark.anyio
        async def test_returns_200_OK(self, get_article_response: Response) -> None:
            assert get_article_response.status_code == 200

        @pytest.mark.anyio
        async def test_returns_json_with_article_data(
            self, get_article_response: Response
        ) -> None:
            assert get_article_response.json() == {
                "article": {
                    "slug": "article-slug",
                    "title": "Article Title",
                    "description": "Article description",
                    "body": "Article description",
                    "tagList": [],
                    "createdAt": "2021-11-26T00:00:00Z",
                    "updatedAt": "2022-12-01T00:00:00Z",
                    "favorited": False,
                    "favoritesCount": 0,
                    "author": {
                        "username": "admin",
                        "bio": "Admin user.",
                        "image": None,
                        "following": False,
                    },
                }
            }
