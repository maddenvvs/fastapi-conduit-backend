from typing import Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.domain.entities.articles import Article, AuthorID, NewArticleDetails
from conduit.domain.repositories.articles import ArticlesRepository
from conduit.infrastructure.persistence.models import ArticleModel
from conduit.infrastructure.time import CurrentTime


def model_to_entity(article_model: ArticleModel) -> Article:
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


class SQLiteArticlesRepository(ArticlesRepository):
    def __init__(self, session: AsyncSession, now: CurrentTime):
        self._session = session
        self._now = now

    async def get_by_slug_or_none(self, slug: str) -> Optional[Article]:
        query = select(ArticleModel).where(ArticleModel.slug == slug)
        if article := await self._session.scalar(query):
            return model_to_entity(article)
        return None

    async def add(
        self,
        author_id: AuthorID,
        article_details: NewArticleDetails,
    ) -> Article:
        current_time = self._now()
        query = (
            insert(ArticleModel)
            .values(
                author_id=author_id,
                slug=article_details.title,
                title=article_details.title,
                description=article_details.description,
                body=article_details.body,
                created_at=current_time,
                updated_at=current_time,
            )
            .returning(ArticleModel)
        )
        result = await self._session.execute(query)
        return model_to_entity(result.scalar_one())
