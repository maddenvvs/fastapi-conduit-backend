from conduit.domain.entities.articles import ArticleWithAuthor, NewArticleDetails
from conduit.domain.entities.users import User
from conduit.domain.services.articles_service import ArticlesService
from conduit.domain.unit_of_work import UnitOfWorkFactory


class CreateArticleUseCase:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        articles_service: ArticlesService,
    ) -> None:
        self._uow_factory = uow_factory
        self._articles_service = articles_service

    async def __call__(
        self,
        article_details: NewArticleDetails,
        current_user: User,
    ) -> ArticleWithAuthor:
        async with self._uow_factory():
            return await self._articles_service.create_article(
                article_details,
                current_user,
            )
