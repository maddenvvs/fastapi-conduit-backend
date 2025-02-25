from typing import Optional, final

from conduit.domain.entities.comments import (
    CommentAuthor,
    CommentWithAuthor,
    NewComment,
)
from conduit.domain.entities.users import User
from conduit.domain.repositories.comments import CommentsRepository
from conduit.domain.services.articles_service import ArticlesService


@final
class CommentsService:
    def __init__(
        self,
        comments_repository: CommentsRepository,
        articles_service: ArticlesService,
    ) -> None:
        self._comments_repository = comments_repository
        self._articles_service = articles_service

    async def add_comment_to_article(
        self,
        slug: str,
        comment_body: str,
        current_user: User,
    ) -> Optional[CommentWithAuthor]:
        article = await self._articles_service.get_article_by_slug(slug, current_user)
        if article is None:
            return None

        comment = await self._comments_repository.add(
            NewComment(
                article_id=article.id,
                author_id=current_user.id,
                body=comment_body,
            )
        )

        author = article.author

        return CommentWithAuthor(
            id=comment.id,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            body=comment.body,
            author=CommentAuthor(
                bio=author.bio,
                username=author.username,
                image=author.image,
                following=author.following,
            ),
        )
