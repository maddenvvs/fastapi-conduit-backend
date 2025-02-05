from conduit.domain.entities.tags import Tag
from conduit.domain.repositories.tags import ITagsRepository


class TagsService:
    def __init__(self, repository: ITagsRepository) -> None:
        self._repository = repository

    async def get_all_tags(self) -> list[Tag]:
        return await self._repository.get_all_tags()
