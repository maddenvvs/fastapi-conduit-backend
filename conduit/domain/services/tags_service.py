import logging
import time
from typing import Final, final

from conduit.domain.entities.tags import Tag
from conduit.domain.repositories.tags import TagsRepository

DEFAULT_LOGGER: Final = logging.getLogger(__name__)

NS_IN_ONE_MS: Final = 1_000_000


@final
class TagsService:
    def __init__(
        self,
        tags_repository: TagsRepository,
        logger: logging.Logger = DEFAULT_LOGGER,
    ) -> None:
        self._tags_repository = tags_repository
        self._logger = logger

    async def get_all_tags(self) -> list[Tag]:
        self._logger.info("Retrieving tags")
        start_time = time.perf_counter_ns()

        try:
            tags = await self._tags_repository.get_all_tags()
        except Exception as ex:
            self._logger.exception("Error retrieving tags", extra={"error": ex})
            raise

        duration_ms = (time.perf_counter_ns() - start_time) / NS_IN_ONE_MS
        self._logger.info(
            "Retrieving tags took %dms",
            duration_ms,
            extra={"duration_ms": duration_ms},
        )
        return tags
