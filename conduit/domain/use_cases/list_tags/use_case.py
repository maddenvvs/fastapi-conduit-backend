from conduit.domain.entities.tags import Tag
from conduit.domain.services.tags_service import TagsService


class ListTagsUseCase:
    def __init__(self, tags_service: TagsService) -> None:
        self._tags_service = tags_service

    async def __call__(self) -> list[Tag]:
        return await self._list_tags()

    async def _list_tags(self) -> list[Tag]:
        return await self._tags_service.get_all_tags()
