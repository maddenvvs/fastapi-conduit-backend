from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert

from conduit.domain.entities.tags import Tag
from conduit.domain.repositories.tags import TagsRepository
from conduit.infrastructure.persistence.models import ArticleTagModel, TagModel
from conduit.infrastructure.persistence.repositories.unit_of_work import (
    SqlAlchemyUnitOfWork,
)
from conduit.infrastructure.time import CurrentTime


def model_to_entity(model: TagModel) -> Tag:
    return Tag(
        id=model.id,
        name=model.name,
    )


class SQLiteTagsRepository(TagsRepository):
    def __init__(self, now: CurrentTime) -> None:
        self._now = now

    async def get_all_tags(self) -> list[Tag]:
        session = SqlAlchemyUnitOfWork.get_current_session()
        query = select(TagModel)
        tags = await session.scalars(query)
        return [model_to_entity(tag_model) for tag_model in tags]

    async def add_many(self, article_id: int, tags: list[str]) -> list[Tag]:
        if len(tags) == 0:
            return []

        session = SqlAlchemyUnitOfWork.get_current_session()
        current_time = self._now()
        insert_query = (
            insert(TagModel)
            .values(
                [
                    dict(
                        name=tag,
                        created_at=current_time,
                    )
                    for tag in tags
                ]
            )
            .on_conflict_do_nothing()
        )
        await session.execute(insert_query)

        select_query = select(TagModel).where(TagModel.name.in_(tags))
        selected_tags = await session.scalars(select_query)
        tags_to_return = [model_to_entity(tag_model) for tag_model in selected_tags]

        link_query = (
            insert(ArticleTagModel)
            .values(
                [
                    dict(
                        article_id=article_id,
                        tag_id=tag.id,
                        created_at=current_time,
                    )
                    for tag in tags_to_return
                ]
            )
            .on_conflict_do_nothing()
        )
        await session.execute(link_query)

        return tags_to_return
