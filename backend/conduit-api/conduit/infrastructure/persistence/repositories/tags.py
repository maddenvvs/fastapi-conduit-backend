from typing import final

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert

from conduit.application.common.repositories.tags import TagsRepository
from conduit.domain.articles.articles import ArticleID
from conduit.domain.tags.tag import Tag
from conduit.infrastructure.persistence.models import ArticleTagModel, TagModel
from conduit.shared.infrastructure.current_time import CurrentTime
from conduit.shared.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork


def _tag_model_to_tag(model: TagModel) -> Tag:
    return Tag(
        id=model.id,
        name=model.name,
    )


@final
class SQLiteTagsRepository(TagsRepository):
    def __init__(self, now: CurrentTime) -> None:
        self._now = now

    async def get_all_tags(self) -> list[Tag]:
        session = SqlAlchemyUnitOfWork.get_current_session()
        query = select(TagModel)
        tags = await session.scalars(query)
        return [_tag_model_to_tag(tag_model) for tag_model in tags]

    async def add_many(self, article_id: int, tags: list[str]) -> list[Tag]:
        if len(tags) == 0:
            return []

        session = SqlAlchemyUnitOfWork.get_current_session()
        current_time = self._now()
        insert_query = (
            insert(TagModel)
            .values(
                [
                    {
                        "name": tag,
                        "created_at": current_time,
                    }
                    for tag in tags
                ],
            )
            .on_conflict_do_nothing()
        )
        await session.execute(insert_query)

        select_query = select(TagModel).where(TagModel.name.in_(tags))
        selected_tags = await session.scalars(select_query)
        tags_to_return = [_tag_model_to_tag(tag_model) for tag_model in selected_tags]

        link_query = (
            insert(ArticleTagModel)
            .values(
                [
                    {
                        "article_id": article_id,
                        "tag_id": tag.id,
                        "created_at": current_time,
                    }
                    for tag in tags_to_return
                ],
            )
            .on_conflict_do_nothing()
        )
        await session.execute(link_query)

        return tags_to_return

    async def list_by_article_id(self, article_id: ArticleID) -> list[Tag]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = (
            select(TagModel, ArticleTagModel)
            .where(
                (ArticleTagModel.article_id == article_id)
                & (ArticleTagModel.tag_id == TagModel.id),
            )
            .order_by(TagModel.created_at.desc())
        )

        tags = await session.scalars(query)
        return [_tag_model_to_tag(tag) for tag in tags]
