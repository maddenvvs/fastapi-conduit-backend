from dataclasses import dataclass
from typing import final

from conduit.domain.entities.articles import BodylessArticleWithAuthor
from conduit.domain.entities.users import UserID
from conduit.domain.repositories.unit_of_work import UnitOfWork


@final
@dataclass(frozen=True)
class FeedArticlesRequest:
    user_id: UserID
    limit: int
    offset: int


@final
@dataclass(frozen=True)
class FeedArticlesResponse:
    articles: list[BodylessArticleWithAuthor]
    articles_count: int


@final
class FeedArticlesUseCase:

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._uow = unit_of_work

    async def __call__(self, feed_request: FeedArticlesRequest) -> FeedArticlesResponse:
        async with self._uow.begin() as db:
            articles = await db.articles.list_by_followings(
                user_id=feed_request.user_id,
                limit=feed_request.limit,
                offset=feed_request.offset,
            )
            articles_count = await db.articles.count_by_followings(feed_request.user_id)

        return FeedArticlesResponse(
            articles=articles,
            articles_count=articles_count,
        )
