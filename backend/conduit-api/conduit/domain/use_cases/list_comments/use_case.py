from typing import Optional, final

from conduit.domain.entities.comments import CommentWithAuthor
from conduit.domain.entities.users import User
from conduit.domain.services.comments_service import CommentsService
from conduit.shared.application.unit_of_work import UnitOfWorkFactory


@final
class ListArticleCommentsUseCase:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        comments_service: CommentsService,
    ) -> None:
        self._uow_factory = uow_factory
        self._comments_service = comments_service

    async def __call__(
        self,
        slug: str,
        current_user: Optional[User],
    ) -> Optional[list[CommentWithAuthor]]:
        async with self._uow_factory():
            return await self._comments_service.list_article_comments(
                slug,
                current_user,
            )
