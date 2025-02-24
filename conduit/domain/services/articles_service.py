from dataclasses import asdict
from typing import Optional, final

from conduit.domain.entities.articles import ArticleAuthor, ArticleWithAuthor
from conduit.domain.entities.users import User
from conduit.domain.exceptions import DomainException
from conduit.domain.repositories.articles import ArticlesRepository
from conduit.domain.repositories.favorites import FavoritesRepository
from conduit.domain.services.profiles_service import ProfilesService


@final
class ArticlesService:
    def __init__(
        self,
        articles_repository: ArticlesRepository,
        profiles_service: ProfilesService,
        favorites_repository: FavoritesRepository,
    ) -> None:
        self._articles_repository = articles_repository
        self._profiles_service = profiles_service
        self._favorites_repository = favorites_repository

    async def get_article_by_slug(
        self, slug: str, current_user: Optional[User]
    ) -> Optional[ArticleWithAuthor]:
        article = await self._articles_repository.get_by_slug_or_none(slug)
        if article is None:
            return None

        author_profile = await self._profiles_service.get_by_user_id_or_none(
            article.author_id
        )
        if author_profile is None:
            raise DomainException("Article cannot exist without an author")

        return ArticleWithAuthor(
            id=article.id,
            slug=article.slug,
            title=article.title,
            description=article.description,
            body=article.description,
            tags=[],
            created_at=article.created_at,
            updated_at=article.updated_at,
            author=ArticleAuthor(
                bio=author_profile.bio,
                following=author_profile.following,
                username=author_profile.username,
                image=author_profile.image,
            ),
        )

    async def favorite_article(
        self,
        slug: str,
        current_user: User,
    ) -> Optional[ArticleWithAuthor]:
        article = await self.get_article_by_slug(slug, current_user)
        if article is None:
            return None

        if article.favorited:
            raise DomainException("Article is already favorited")

        await self._favorites_repository.add(
            article_id=article.id,
            user_id=current_user.id,
        )

        return ArticleWithAuthor(
            **asdict(article),
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
            raise DomainException("Article is already unfavorited")

        await self._favorites_repository.delete(
            article_id=article.id,
            user_id=current_user.id,
        )

        return ArticleWithAuthor(
            **asdict(article),
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
            raise DomainException("Article not found")

        if article.author_id != current_user.id:
            raise DomainException("You don't own the article")

        await self._articles_repository.delete_by_id(article.id)
