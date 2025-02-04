from conduit.domain.entities.tags import Tag
from conduit.domain.repositories.tags import ITagsRepository

TAGS = [
    Tag("reactjs"),
    Tag("angularjs"),
]


class InMemoryTagsRepository(ITagsRepository):

    async def get_all_tags(self) -> list[Tag]:
        return TAGS
