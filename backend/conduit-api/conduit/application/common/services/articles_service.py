from typing import Optional, final

from conduit.application.articles.services.slug_service import SlugService
from conduit.application.common.errors import Errors
from conduit.application.common.repositories.articles import ArticlesRepository
from conduit.application.common.repositories.favorites import FavoritesRepository
from conduit.application.common.repositories.tags import TagsRepository
from conduit.application.common.services.profiles_service import ProfilesService
from conduit.domain.articles.articles import (
    Article,
    ArticleAuthor,
    ArticleWithAuthor,
    NewArticleDetails,
    NewArticleDetailsWithSlug,
    UpdateArticleFields,
)
from conduit.domain.profiles.profile import Profile
from conduit.domain.users.user import User


@final
class ArticlesService:
    def __init__(
        self,
        articles_repository: ArticlesRepository,
        tags_repository: TagsRepository,
        profiles_service: ProfilesService,
        favorites_repository: FavoritesRepository,
        slug_service: SlugService,
    ) -> None:
        self._articles_repository = articles_repository
        self._tags_repository = tags_repository
        self._profiles_service = profiles_service
        self._favorites_repository = favorites_repository
        self._slug_service = slug_service

    async def get_article_by_slug(
        self,
        slug: str,
        current_user: Optional[User],
    ) -> Optional[ArticleWithAuthor]:
        article = await self._articles_repository.get_by_slug_or_none(slug)
        if article is None:
            return None

        author_profile = await self._profiles_service.get_by_user_id_or_none(
            article.author_id,
            current_user,
        )
        if author_profile is None:
            raise Errors.article_without_author()

        return await self._get_article_info(article, author_profile, current_user)

    async def create_article(
        self,
        article_details: NewArticleDetails,
        current_user: User,
    ) -> ArticleWithAuthor:
        profile = await self._profiles_service.get_by_user_id_or_none(current_user.id)
        if profile is None:
            raise Errors.profile_not_found()

        slugged_article = NewArticleDetailsWithSlug(
            title=article_details.title,
            description=article_details.description,
            body=article_details.body,
            slug=self._slug_service.slugify_string(article_details.title),
            tags=article_details.tags,
        )

        created_article = await self._articles_repository.add(
            current_user.id,
            slugged_article,
        )
        await self._tags_repository.add_many(
            created_article.id,
            article_details.tags,
        )

        return ArticleWithAuthor(
            id=created_article.id,
            slug=created_article.slug,
            description=created_article.description,
            body=created_article.body,
            title=created_article.title,
            created_at=created_article.created_at,
            updated_at=created_article.updated_at,
            author=ArticleAuthor(
                username=profile.username,
                bio=profile.bio,
                image=profile.image,
                following=profile.following,
            ),
            tags=article_details.tags,
            favorited=False,
            favorites_count=0,
        )

    async def update_article(
        self,
        slug: str,
        update_fields: UpdateArticleFields,
        current_user: User,
    ) -> Optional[ArticleWithAuthor]:
        article = await self._articles_repository.get_by_slug_or_none(slug)
        if article is None:
            return None

        if article.author_id != current_user.id:
            raise Errors.article_owning_error()

        if update_fields.title:
            update_fields.slug = self._slug_service.slugify_string(update_fields.title)

        article = await self._articles_repository.update_by_slug(slug, update_fields)
        author_profile = await self._profiles_service.get_by_user_id_or_none(
            article.author_id,
            current_user,
        )
        if author_profile is None:
            raise Errors.article_without_author()

        return await self._get_article_info(article, author_profile, current_user)

    async def favorite_article(
        self,
        slug: str,
        current_user: User,
    ) -> Optional[ArticleWithAuthor]:
        article = await self.get_article_by_slug(slug, current_user)
        if article is None:
            return None

        if article.favorited:
            raise Errors.article_is_already_favorited()

        await self._favorites_repository.add(
            article_id=article.id,
            user_id=current_user.id,
        )

        return ArticleWithAuthor(
            id=article.id,
            slug=article.slug,
            title=article.title,
            description=article.description,
            body=article.body,
            tags=article.tags,
            created_at=article.created_at,
            updated_at=article.updated_at,
            author=article.author,
            favorited=True,
            favorites_count=article.favorites_count + 1,
        )

    async def unfavorite_article(
        self,
        slug: str,
        current_user: User,
    ) -> Optional[ArticleWithAuthor]:
        article = await self.get_article_by_slug(slug, current_user)
        if article is None:
            return None

        if not article.favorited:
            raise Errors.article_is_already_unfavorited()

        await self._favorites_repository.delete(
            article_id=article.id,
            user_id=current_user.id,
        )

        return ArticleWithAuthor(
            id=article.id,
            slug=article.slug,
            title=article.title,
            description=article.description,
            body=article.body,
            tags=article.tags,
            created_at=article.created_at,
            updated_at=article.updated_at,
            author=article.author,
            favorited=False,
            favorites_count=article.favorites_count - 1,
        )

    async def delete_by_slug(
        self,
        slug: str,
        current_user: User,
    ) -> None:
        article = await self._articles_repository.get_by_slug_or_none(slug)
        if article is None:
            raise Errors.article_not_found()

        if article.author_id != current_user.id:
            raise Errors.article_owning_error()

        await self._articles_repository.delete_by_id(article.id)

    async def _get_article_info(
        self,
        article: Article,
        profile: Profile,
        current_user: Optional[User],
    ) -> ArticleWithAuthor:
        tags = await self._tags_repository.list_by_article_id(article.id)
        tag_names = [tag.name for tag in tags]

        favorites_count = await self._favorites_repository.count(article.id)
        is_favorited = (
            await self._favorites_repository.exists(
                current_user.id,
                article.id,
            )
            if current_user
            else False
        )
        return ArticleWithAuthor(
            id=article.id,
            slug=article.slug,
            title=article.title,
            description=article.description,
            body=article.body,
            tags=tag_names,
            created_at=article.created_at,
            updated_at=article.updated_at,
            favorited=is_favorited,
            favorites_count=favorites_count,
            author=ArticleAuthor(
                username=profile.username,
                bio=profile.bio,
                image=profile.image,
                following=profile.following,
            ),
        )
