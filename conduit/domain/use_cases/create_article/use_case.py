from conduit.domain.entities.articles import (
    ArticleAuthor,
    ArticleWithAuthor,
    NewArticleDetails,
    NewArticleDetailsWithSlug,
)
from conduit.domain.entities.users import User
from conduit.domain.exceptions import DomainException
from conduit.domain.repositories.articles import ArticlesRepository
from conduit.domain.repositories.tags import TagsRepository
from conduit.domain.services.profiles_service import ProfilesService
from conduit.domain.services.slug_service import SlugService
from conduit.domain.unit_of_work import UnitOfWorkFactory


class CreateArticleUseCase:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        profiles_service: ProfilesService,
        slug_service: SlugService,
        tags_repository: TagsRepository,
        articles_repository: ArticlesRepository,
    ) -> None:
        self._uow_factory = uow_factory
        self._profiles_service = profiles_service
        self._slug_service = slug_service
        self._tags_repository = tags_repository
        self._articles_repository = articles_repository

    async def __call__(
        self,
        article_details: NewArticleDetails,
        current_user: User,
    ) -> ArticleWithAuthor:
        async with self._uow_factory():
            profile = await self._profiles_service.get_by_user_id_or_none(
                current_user.id
            )
            if profile is None:
                raise DomainException("Profile not found")

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
