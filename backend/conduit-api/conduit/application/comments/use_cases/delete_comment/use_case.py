from typing import final

from conduit.application.comments.services.comments_service import CommentsService
from conduit.domain.entities.comments import CommentID
from conduit.domain.entities.users import User
from conduit.shared.application.unit_of_work import UnitOfWorkFactory


@final
class DeleteArticleCommentUseCase:
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
        comment_id: CommentID,
        current_user: User,
    ) -> bool:
        async with self._uow_factory():
            return await self._comments_service.delete_comment(
                slug,
                comment_id,
                current_user,
            )
