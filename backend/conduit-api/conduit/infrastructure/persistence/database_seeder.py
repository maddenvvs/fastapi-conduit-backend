from conduit.infrastructure.persistence.models import TagModel
from conduit.shared.infrastructure.current_time import CurrentTime
from conduit.shared.infrastructure.persistence.database import Database


class DatabaseSeeder:
    def __init__(self, db: Database, now: CurrentTime) -> None:
        self._db = db
        self._now = now

    async def seed_database(self) -> None:
        current_time = self._now()

        available_tags = [
            "android",
            "python3",
            "clean-code",
            "music",
            "films",
            "review",
            "javascript",
            "typescript",
            "politics",
            "сюрприз с пробелами",  # noqa: RUF001
            "😎 leetcode",
        ]
        async with self._db.create_session() as session:
            session.add_all(
                (
                    TagModel(
                        id=i,
                        name=name,
                        created_at=current_time,
                    )
                    for i, name in enumerate(available_tags, start=1)
                ),
            )
            await session.commit()
