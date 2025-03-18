from typing import Optional, final

from conduit.application.common.errors import Errors
from conduit.application.common.repositories.comments import CommentsRepository
from conduit.application.common.services.articles_service import ArticlesService
from conduit.application.common.services.profiles_service import ProfilesService
from conduit.domain.comments.comments import (
    Comment,
    CommentAuthor,
    CommentID,
    CommentWithAuthor,
    NewComment,
)
from conduit.domain.profiles.profile import Profile, ProfileID
from conduit.domain.users.user import User


def _to_comment_with_author(comment: Comment, author: Profile) -> CommentWithAuthor:
    return CommentWithAuthor(
        id=comment.id,
        body=comment.body,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        author=CommentAuthor(
            username=author.username,
            bio=author.bio,
            image=author.image,
            following=author.following,
        ),
    )


@final
class CommentsService:
    def __init__(
        self,
        comments_repository: CommentsRepository,
        articles_service: ArticlesService,
        profiles_service: ProfilesService,
    ) -> None:
        self._comments_repository = comments_repository
        self._articles_service = articles_service
        self._profiles_service = profiles_service

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
            ),
        )

        author = current_user
        return CommentWithAuthor(
            id=comment.id,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            body=comment.body,
            author=CommentAuthor(
                bio=author.bio,
                username=author.username,
                image=author.image,
                following=False,
            ),
        )

    async def list_article_comments(
        self,
        slug: str,
        current_user: Optional[User],
    ) -> Optional[list[CommentWithAuthor]]:
        article = await self._articles_service.get_article_by_slug(slug, current_user)
        if article is None:
            return None

        raw_comments = await self._comments_repository.list_by_article_id(article.id)
        profiles_map = await self._get_profiles_map(raw_comments, current_user)

        return [
            _to_comment_with_author(
                comment,
                profiles_map[comment.author_id],
            )
            for comment in raw_comments
        ]

    async def delete_comment(
        self,
        slug: str,
        comment_id: CommentID,
        current_user: User,
    ) -> bool:
        article = await self._articles_service.get_article_by_slug(slug, current_user)
        if article is None:
            return False

        comment = await self._comments_repository.get(comment_id)
        if comment.author_id != current_user.id:
            raise Errors.comment_ownership()

        await self._comments_repository.delete(comment_id)

        return True

    async def _get_profiles_map(
        self,
        comments: list[Comment],
        current_user: Optional[User],
    ) -> dict[ProfileID, Profile]:
        user_ids = [comment.author_id for comment in comments]
        profiles = await self._profiles_service.list_by_user_ids(user_ids, current_user)
        return {profile.id: profile for profile in profiles}
