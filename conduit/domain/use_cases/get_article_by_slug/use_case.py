from typing import Optional

from conduit.domain.entities.articles import ArticleWithAuthor
from conduit.domain.entities.users import User
from conduit.domain.repositories.unit_of_work import UnitOfWork


class GetArticleBySlugUseCase:
    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._uow = unit_of_work

    async def __call__(
        self,
        slug: str,
        current_user: Optional[User],
    ) -> ArticleWithAuthor:
        raise NotImplementedError
