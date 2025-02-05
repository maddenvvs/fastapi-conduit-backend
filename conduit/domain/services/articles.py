from typing import Optional

from conduit.domain.entities.articles import Article
from conduit.domain.repositories.articles import IArticlesRepository


class ArticlesService:
    def __init__(self, repository: IArticlesRepository) -> None:
        self._repository = repository

    async def find_article_by_slug(self, slug: str) -> Optional[Article]:
        return await self._repository.find_article_by_slug(slug)
