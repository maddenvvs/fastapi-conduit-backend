from dataclasses import asdict

from conduit.domain.entities.articles import (
    ArticleAuthor,
    ArticleWithAuthor,
    AuthorID,
    NewArticleDetails,
)
from conduit.domain.repositories.unit_of_work import UnitOfWork
from conduit.domain.services.profiles_service import ProfilesService
from conduit.domain.use_cases.create_article.exceptions import (
    ArticleProfileMissingException,
)


class CreateArticleUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        profiles_service: ProfilesService,
    ) -> None:
        self._uow = unit_of_work
        self._profiles_service = profiles_service

    async def __call__(
        self,
        article_details: NewArticleDetails,
        author_id: AuthorID,
    ) -> ArticleWithAuthor:
        profile = await self._profiles_service.get_by_user_id_or_none(author_id)
        if profile is None:
            raise ArticleProfileMissingException

        async with self._uow.begin() as db:
            created_article = await db.articles.add(author_id, article_details)
            await db.tags.add_many(created_article.id, article_details.tags)

        return ArticleWithAuthor(
            **asdict(created_article),
            author=ArticleAuthor(
                username=profile.username,
                bio=profile.bio,
                image=profile.image,
                following=profile.following,
            ),
            tags=article_details.tags,
        )
