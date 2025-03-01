from typing import Any, Optional

from sqlalchemy import delete, exists, func, insert, select, true, update
from sqlalchemy.orm import aliased
from sqlalchemy.sql.functions import count

from conduit.domain.entities.articles import (
    Article,
    ArticleAuthor,
    ArticleID,
    AuthorID,
    BodylessArticleWithAuthor,
    NewArticleDetailsWithSlug,
    UpdateArticleFields,
)
from conduit.domain.entities.users import UserID
from conduit.domain.repositories.articles import ArticlesRepository
from conduit.infrastructure.current_time import CurrentTime
from conduit.infrastructure.persistence.models import (
    ArticleModel,
    ArticleTagModel,
    FavoriteModel,
    FollowerModel,
    TagModel,
    UserModel,
)
from conduit.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork

ArticleAliased = aliased(ArticleModel)


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
            image=row.image_url,
            following=row.following,
        ),
    )


class SQLiteArticlesRepository(ArticlesRepository):
    def __init__(self, now: CurrentTime):
        self._now = now

    async def get_by_slug_or_none(self, slug: str) -> Optional[Article]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(ArticleModel).where(ArticleModel.slug == slug)
        if article := await session.scalar(query):
            return _model_to_entity(article)
        return None

    async def add(
        self,
        author_id: AuthorID,
        article_details: NewArticleDetailsWithSlug,
    ) -> Article:
        session = SqlAlchemyUnitOfWork.get_current_session()
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
        result = await session.execute(query)
        return _model_to_entity(result.scalar_one())

    async def list_by_followings(
        self,
        user_id: UserID,
        limit: int,
        offset: int,
    ) -> list[BodylessArticleWithAuthor]:
        session = SqlAlchemyUnitOfWork.get_current_session()

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
                .where(FavoriteModel.article_id == ArticleModel.id)
                .scalar_subquery()
                .label("favorites_count"),
                # Subquery to check if favorited by user with id `user_id`.
                exists()
                .where(
                    (FavoriteModel.user_id == user_id)
                    & (FavoriteModel.article_id == ArticleModel.id)
                )
                .label("favorited"),
                # Concatenate tags.
                func.group_concat(TagModel.name, ", ").label("tags"),
            )
            .join(
                UserModel,
                ArticleModel.author_id == UserModel.id,
            )
            .join(ArticleTagModel, ArticleTagModel.article_id == ArticleModel.id)
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
        articles = await session.execute(query)

        return [_to_bodyless_article(row) for row in articles]

    async def count_by_followings(self, user_id: UserID) -> int:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(count(ArticleModel.id)).join(
            FollowerModel,
            (FollowerModel.follower_id == user_id)
            & (FollowerModel.following_id == ArticleModel.author_id),
        )

        result = await session.execute(query)
        return result.scalar_one()

    async def list_by_filters(
        self,
        user_id: Optional[UserID],
        limit: int,
        offset: int,
        tag: Optional[str],
        author: Optional[str],
        favorited: Optional[str],
    ) -> list[BodylessArticleWithAuthor]:
        session = SqlAlchemyUnitOfWork.get_current_session()

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
                exists()
                .where(
                    (FollowerModel.follower_id == user_id)
                    & (FollowerModel.following_id == ArticleModel.author_id)
                )
                .label("following"),
                # Subquery for favorites count.
                select(func.count())
                .select_from(FavoriteModel)
                .join(ArticleModel, ArticleModel.id == FavoriteModel.article_id)
                .where(FavoriteModel.article_id == ArticleModel.id)
                .scalar_subquery()
                .label("favorites_count"),
                # Subquery to check if favorited by user with id `user_id`.
                select(FavoriteModel.article_id)
                .where(
                    (FavoriteModel.user_id == user_id)
                    & (FavoriteModel.article_id == ArticleModel.id)
                )
                .exists()
                .correlate(FavoriteModel, ArticleModel)
                .label("favorited"),
                # Concatenate tags.
                func.group_concat(TagModel.name, ", ").label("tags"),
            )
            .outerjoin(
                UserModel,
                ArticleModel.author_id == UserModel.id,
            )
            .outerjoin(ArticleTagModel, ArticleTagModel.article_id == ArticleModel.id)
            .outerjoin(FavoriteModel, FavoriteModel.article_id == ArticleModel.id)
            .outerjoin(TagModel, TagModel.id == ArticleTagModel.tag_id)
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
            .order_by(ArticleModel.created_at.desc())
        )

        if tag is not None:
            query = query.where(
                select(TagModel.id)
                .select_from(TagModel)
                .join(ArticleTagModel, ArticleTagModel.tag_id == TagModel.id)
                .join(ArticleAliased, ArticleAliased.id == ArticleTagModel.article_id)
                .where(ArticleAliased.id == ArticleModel.id, TagModel.name == tag)
                .exists()
            )
        if author is not None:
            query = query.where(UserModel.username == author)
        if favorited is not None:
            query = query.where(
                FavoriteModel.user_id
                == select(UserModel.id)
                .where(UserModel.username == favorited)
                .scalar_subquery()
            )

        query = query.limit(limit).offset(offset)
        articles = await session.execute(query)

        return [_to_bodyless_article(row) for row in articles]

    async def count_by_filters(
        self,
        tag: Optional[str],
        author: Optional[str],
        favorited: Optional[str],
    ) -> int:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(count(ArticleModel.id))

        if tag is not None:
            query = query.join(
                ArticleTagModel, ArticleTagModel.article_id == ArticleModel.id
            ).where(
                ArticleTagModel.tag_id
                == select(TagModel.id).where(TagModel.name == tag).scalar_subquery()
            )

        if author is not None:
            query = query.join(UserModel, UserModel.id == ArticleModel.author_id).where(
                UserModel.username == author
            )

        if favorited is not None:
            query = query.join(
                FavoriteModel, FavoriteModel.article_id == ArticleModel.id
            ).where(
                FavoriteModel.user_id
                == select(UserModel.id)
                .where(UserModel.username == favorited)
                .scalar_subquery()
            )

        result = await session.execute(query)
        return result.scalar_one()

    async def delete_by_id(self, article_id: ArticleID) -> None:
        session = SqlAlchemyUnitOfWork.get_current_session()
        query = delete(ArticleModel).where(ArticleModel.id == article_id)
        await session.execute(query)

    async def update_by_slug(
        self, slug: str, update_fields: UpdateArticleFields
    ) -> Article:
        session = SqlAlchemyUnitOfWork.get_current_session()
        current_time = self._now()

        query = (
            update(ArticleModel)
            .where(ArticleModel.slug == slug)
            .values(
                updated_at=current_time,
            )
            .returning(ArticleModel)
        )

        if update_fields.title is not None:
            query = query.values(
                title=update_fields.title,
                slug=update_fields.slug,
            )
        if update_fields.description is not None:
            query = query.values(description=update_fields.description)
        if update_fields.body is not None:
            query = query.values(body=update_fields.body)

        result = await session.execute(query)
        return _model_to_entity(result.scalar_one())
