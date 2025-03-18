from typing import Optional, final

from conduit.application.comments.services.comments_service import CommentsService
from conduit.domain.comments.comments import CommentWithAuthor
from conduit.domain.users.user import User
from conduit.shared.application.unit_of_work import UnitOfWorkFactory


@final
class AddCommentToArticleUseCase:
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
        comment_body: str,
        current_user: User,
    ) -> Optional[CommentWithAuthor]:
        async with self._uow_factory():
            return await self._comments_service.add_comment_to_article(
                slug,
                comment_body,
                current_user,
            )
