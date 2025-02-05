from typing import Annotated

from fastapi import Depends

from conduit.domain.repositories.articles import IArticlesRepository
from conduit.domain.repositories.tags import ITagsRepository
from conduit.domain.services.articles import ArticlesService
from conduit.domain.services.tags import TagsService
from conduit.persistence.repositories.articles import InMemoryArticlesRepository
from conduit.persistence.repositories.tags import InMemoryTagsRepository


async def create_tags_repository() -> ITagsRepository:
    return InMemoryTagsRepository()


async def create_tags_service(
    repository: Annotated[ITagsRepository, Depends(create_tags_repository)]
) -> TagsService:
    return TagsService(repository=repository)


async def create_articles_repository() -> IArticlesRepository:
    return InMemoryArticlesRepository()


async def create_articles_service(
    repository: Annotated[IArticlesRepository, Depends(create_articles_repository)]
) -> ArticlesService:
    return ArticlesService(repository=repository)


ITagsService = Annotated[TagsService, Depends(create_tags_service)]
IArticlesService = Annotated[ArticlesService, Depends(create_articles_service)]
