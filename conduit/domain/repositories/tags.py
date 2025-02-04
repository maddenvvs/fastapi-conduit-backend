import abc

from conduit.domain.entities.tags import Tag


class ITagsRepository(abc.ABC):

    @abc.abstractmethod
    async def get_all_tags(self) -> list[Tag]: ...
