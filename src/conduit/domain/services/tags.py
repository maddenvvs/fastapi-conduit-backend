import logging
import time
from typing import Final, final

from conduit.domain.entities.tags import Tag
from conduit.domain.repositories.unit_of_work import UnitOfWork

DEFAULT_LOGGER: Final = logging.getLogger(__name__)

NS_IN_ONE_MS: Final = 1_000_000


@final
class TagsService:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        logger: logging.Logger = DEFAULT_LOGGER,
    ) -> None:
        self._uow = unit_of_work
        self._logger = logger

    async def get_all_tags(self) -> list[Tag]:
        self._logger.info("Retrieving tags")
        start_time = time.perf_counter_ns()

        try:
            async with self._uow.begin() as db:
                tags = await db.tags.get_all_tags()
        except Exception as ex:
            self._logger.error("Error retrieving tags", extra=dict(error=ex))
            raise

        duration_ms = (time.perf_counter_ns() - start_time) / NS_IN_ONE_MS
        self._logger.info(
            "Retrieving tags took %dms",
            duration_ms,
            extra=dict(duration_ms=duration_ms),
        )
        return tags
