from typing import final

from conduit.application.common.services.articles_service import ArticlesService
from conduit.domain.users.user import User
from conduit.shared.application.unit_of_work import UnitOfWorkFactory


@final
class DeleteArticleBySlugUseCase:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        articles_service: ArticlesService,
    ) -> None:
        self._uow_factory = uow_factory
        self._articles_service = articles_service

    async def __call__(self, slug: str, current_user: User) -> None:
        async with self._uow_factory():
            await self._articles_service.delete_by_slug(slug, current_user)
