from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.domain.entities.tags import Tag
from conduit.domain.repositories.tags import ITagsRepository
from conduit.persistence.models import TagModel

TAGS = [
    Tag("reactjs"),
    Tag("angularjs"),
]


class InMemoryTagsRepository(ITagsRepository):

    async def get_all_tags(self) -> list[Tag]:
        return TAGS


def model_to_entity(model: TagModel) -> Tag:
    return Tag(
        name=model.name,
    )


class SQLiteTagsRepository(ITagsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all_tags(self) -> list[Tag]:
        query = select(TagModel)
        tags = await self._session.scalars(query)
        return [model_to_entity(tag_model) for tag_model in tags]
