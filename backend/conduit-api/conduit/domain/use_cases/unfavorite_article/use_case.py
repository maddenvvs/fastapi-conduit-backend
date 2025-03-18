from typing import Optional, final

from conduit.domain.entities.articles import ArticleWithAuthor
from conduit.domain.entities.users import User
from conduit.domain.services.articles_service import ArticlesService
from conduit.shared.application.unit_of_work import UnitOfWorkFactory


@final
class UnfavoriteArticleUseCase:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        articles_service: ArticlesService,
    ) -> None:
        self._uow_factory = uow_factory
        self._articles_service = articles_service

    async def __call__(
        self,
        slug: str,
        current_user: User,
    ) -> Optional[ArticleWithAuthor]:
        async with self._uow_factory():
            return await self._articles_service.unfavorite_article(slug, current_user)
