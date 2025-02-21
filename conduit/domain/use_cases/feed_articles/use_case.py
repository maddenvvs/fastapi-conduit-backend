from dataclasses import dataclass
from typing import final

from conduit.domain.entities.articles import BodylessArticleWithAuthor
from conduit.domain.entities.users import UserID
from conduit.domain.repositories.articles import ArticlesRepository
from conduit.domain.unit_of_work import UnitOfWorkFactory


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

    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        articles_repository: ArticlesRepository,
    ) -> None:
        self._uof_factory = uow_factory
        self._articles_repository = articles_repository

    async def __call__(self, feed_request: FeedArticlesRequest) -> FeedArticlesResponse:
        async with self._uof_factory():
            articles = await self._articles_repository.list_by_followings(
                user_id=feed_request.user_id,
                limit=feed_request.limit,
                offset=feed_request.offset,
            )
            articles_count = await self._articles_repository.count_by_followings(
                feed_request.user_id
            )

        return FeedArticlesResponse(
            articles=articles,
            articles_count=articles_count,
        )
