from conduit.domain.entities.tags import Tag
from conduit.domain.services.tags_service import TagsService
from conduit.domain.unit_of_work import UnitOfWorkFactory


class ListTagsUseCase:
    def __init__(
        self,
        tags_service: TagsService,
        uow_factory: UnitOfWorkFactory,
    ) -> None:
        self._tags_service = tags_service
        self._uow_factory = uow_factory

    async def __call__(self) -> list[Tag]:
        return await self._list_tags()

    async def _list_tags(self) -> list[Tag]:
        async with self._uow_factory():
            return await self._tags_service.get_all_tags()
