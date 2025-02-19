from typing import Any, Optional

from sqlalchemy import exists, func, insert, select, true
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from conduit.domain.entities.articles import (
    Article,
    ArticleAuthor,
    AuthorID,
    BodylessArticleWithAuthor,
    NewArticleDetailsWithSlug,
)
from conduit.domain.entities.users import UserID
from conduit.domain.repositories.articles import ArticlesRepository
from conduit.infrastructure.persistence.models import (
    ArticleModel,
    ArticleTagModel,
    FavoriteModel,
    FollowerModel,
    TagModel,
    UserModel,
)
from conduit.infrastructure.time import CurrentTime


def _model_to_entity(article_model: ArticleModel) -> Article:
    return Article(
        id=article_model.id,
        author_id=article_model.author_id,
        body=article_model.body,
        title=article_model.title,
        description=article_model.description,
        slug=article_model.slug,
        created_at=article_model.created_at,
        updated_at=article_model.updated_at,
    )


def _to_bodyless_article(row: Any) -> BodylessArticleWithAuthor:
    return BodylessArticleWithAuthor(
        slug=row.slug,
        title=row.title,
        description=row.description,
        tags=row.tags.split(", ") if row.tags else [],
        created_at=row.created_at,
        updated_at=row.updated_at,
        favorited=row.favorited,
        favorites_count=row.favorites_count,
        author=ArticleAuthor(
            username=row.username,
            bio=row.bio,
            image=row.image,
            following=row.following,
        ),
    )


class SQLiteArticlesRepository(ArticlesRepository):
    def __init__(self, session: AsyncSession, now: CurrentTime):
        self._session = session
        self._now = now

    async def get_by_slug_or_none(self, slug: str) -> Optional[Article]:
        query = select(ArticleModel).where(ArticleModel.slug == slug)
        if article := await self._session.scalar(query):
            return _model_to_entity(article)
        return None

    async def add(
        self,
        author_id: AuthorID,
        article_details: NewArticleDetailsWithSlug,
    ) -> Article:
        current_time = self._now()
        query = (
            insert(ArticleModel)
            .values(
                author_id=author_id,
                slug=article_details.slug,
                title=article_details.title,
                description=article_details.description,
                body=article_details.body,
                created_at=current_time,
                updated_at=current_time,
            )
            .returning(ArticleModel)
        )
        result = await self._session.execute(query)
        return _model_to_entity(result.scalar_one())

    async def list_by_followings(
        self, user_id: UserID, limit: int, offset: int
    ) -> list[BodylessArticleWithAuthor]:
        query = (
            select(
                ArticleModel.id.label("id"),
                ArticleModel.author_id.label("author_id"),
                ArticleModel.slug.label("slug"),
                ArticleModel.title.label("title"),
                ArticleModel.description.label("description"),
                ArticleModel.created_at.label("created_at"),
                ArticleModel.updated_at.label("updated_at"),
                UserModel.id.label("user_id"),
                UserModel.username.label("username"),
                UserModel.bio.label("bio"),
                UserModel.email.label("email"),
                UserModel.image_url.label("image_url"),
                true().label("following"),
                # Subquery for favorites count.
                select(func.count(FavoriteModel.article_id))
                .where(FavoriteModel.article_id == Article.id)
                .scalar_subquery()
                .label("favorites_count"),
                # Subquery to check if favorited by user with id `user_id`.
                exists()
                .where(
                    (FavoriteModel.user_id == user_id)
                    & (FavoriteModel.article_id == Article.id)
                )
                .label("favorited"),
                # Concatenate tags.
                func.string_agg(TagModel.name, ", ").label("tags"),
            )
            .join(
                UserModel,
                ArticleModel.author_id == UserModel.id,
            )
            .join(ArticleTagModel, ArticleTagModel.article_id == Article.id)
            .join(TagModel, TagModel.id == ArticleTagModel.tag_id)
            .filter(
                UserModel.id.in_(
                    select(FollowerModel.following_id)
                    .where(FollowerModel.follower_id == user_id)
                    .scalar_subquery()
                )
            )
            .group_by(
                ArticleModel.id,
                ArticleModel.author_id,
                ArticleModel.slug,
                ArticleModel.title,
                ArticleModel.description,
                ArticleModel.created_at,
                ArticleModel.updated_at,
                UserModel.id,
                UserModel.username,
                UserModel.bio,
                UserModel.email,
                UserModel.image_url,
            )
        )

        query = query.limit(limit).offset(offset)
        articles = await self._session.execute(query)

        return [_to_bodyless_article(row) for row in articles]

    async def count_by_followings(self, user_id: UserID) -> int:
        query = select(count(ArticleModel.id)).join(
            FollowerModel,
            FollowerModel.follower_id == user_id
            and FollowerModel.following_id == ArticleModel.id,
        )

        result = await self._session.execute(query)
        return result.scalar_one()
