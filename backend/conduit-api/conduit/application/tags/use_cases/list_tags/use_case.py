from typing import final

from conduit.application.tags.services.tags_service import TagsService
from conduit.domain.entities.tags import Tag
from conduit.shared.application.unit_of_work import UnitOfWorkFactory


@final
class ListTagsUseCase:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        tags_service: TagsService,
    ) -> None:
        self._uow_factory = uow_factory
        self._tags_service = tags_service

    async def __call__(self) -> list[Tag]:
        async with self._uow_factory():
            return await self._tags_service.get_all_tags()
