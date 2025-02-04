from typing import Annotated

from fastapi import Depends

from conduit.domain.repositories.tags import ITagsRepository
from conduit.domain.services.tags import TagsService
from conduit.persistence.repositories.tags import InMemoryTagsRepository


async def create_tags_repository() -> ITagsRepository:
    return InMemoryTagsRepository()


async def create_tags_service(
    repository: Annotated[ITagsRepository, Depends(create_tags_repository)]
) -> TagsService:
    return TagsService(repository=repository)


ITagsService = Annotated[TagsService, Depends(create_tags_service)]
