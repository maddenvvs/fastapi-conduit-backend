from conduit.domain.entities.articles import (
    ArticleAuthor,
    ArticleWithAuthor,
    AuthorID,
    NewArticleDetails,
    NewArticleDetailsWithSlug,
)
from conduit.domain.repositories.tags import TagsRepository
from conduit.domain.repositories.unit_of_work import UnitOfWork
from conduit.domain.services.profiles_service import ProfilesService
from conduit.domain.services.slug_service import SlugService
from conduit.domain.unit_of_work import UnitOfWorkFactory
from conduit.domain.use_cases.create_article.exceptions import (
    ArticleProfileMissingException,
)


class CreateArticleUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        uow_factory: UnitOfWorkFactory,
        profiles_service: ProfilesService,
        slug_service: SlugService,
        tags_repository: TagsRepository,
    ) -> None:
        self._uow = unit_of_work
        self._uow_factory = uow_factory
        self._profiles_service = profiles_service
        self._slug_service = slug_service
        self._tags_repository = tags_repository

    async def __call__(
        self,
        article_details: NewArticleDetails,
        author_id: AuthorID,
    ) -> ArticleWithAuthor:
        profile = await self._profiles_service.get_by_user_id_or_none(author_id)
        if profile is None:
            raise ArticleProfileMissingException

        slugged_article = NewArticleDetailsWithSlug(
            title=article_details.title,
            description=article_details.description,
            body=article_details.body,
            slug=self._slug_service.slugify_string(article_details.title),
            tags=article_details.tags,
        )

        async with self._uow.begin() as db, self._uow_factory():
            created_article = await db.articles.add(author_id, slugged_article)
            await self._tags_repository.add_many(
                created_article.id,
                article_details.tags,
            )

        return ArticleWithAuthor(
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
        )
