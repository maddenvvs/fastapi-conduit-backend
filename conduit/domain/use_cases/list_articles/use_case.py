from dataclasses import dataclass
from typing import Optional, final

from conduit.domain.entities.articles import BodylessArticleWithAuthor
from conduit.domain.entities.users import User
from conduit.domain.repositories.unit_of_work import UnitOfWork


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
    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._uow = unit_of_work

    async def __call__(
        self,
        list_articles_request: ListArticlesRequest,
    ) -> ListArticlesResponse:
        user = list_articles_request.user
        user_id = user.id if user else None

        async with self._uow.begin() as db:
            articles = await db.articles.list_by_filters(
                user_id=user_id,
                limit=list_articles_request.limit,
                offset=list_articles_request.offset,
            )
            articles_count = await db.articles.count_by_filters()

        return ListArticlesResponse(
            articles=articles,
            articles_count=articles_count,
        )
