from dataclasses import dataclass
from typing import Optional, final

from conduit.domain.entities.articles import BodylessArticleWithAuthor
from conduit.domain.entities.users import User
from conduit.domain.repositories.articles import ArticlesRepository
from conduit.domain.unit_of_work import UnitOfWorkFactory


@final
@dataclass(frozen=True)
class ListArticlesRequest:
    limit: int
    offset: int
    user: Optional[User]


@final
@dataclass(frozen=True)
class ListArticlesResponse:
    articles: list[BodylessArticleWithAuthor]
    articles_count: int


@final
class ListArticlesUseCase:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        articles_repository: ArticlesRepository,
    ) -> None:
        self._uow_factory = uow_factory
        self._articles_repository = articles_repository

    async def __call__(
        self,
        list_articles_request: ListArticlesRequest,
    ) -> ListArticlesResponse:
        user = list_articles_request.user
        user_id = user.id if user else None

        async with self._uow_factory():
            articles = await self._articles_repository.list_by_filters(
                user_id=user_id,
                limit=list_articles_request.limit,
                offset=list_articles_request.offset,
            )
            articles_count = await self._articles_repository.count_by_filters()

        return ListArticlesResponse(
            articles=articles,
            articles_count=articles_count,
        )
