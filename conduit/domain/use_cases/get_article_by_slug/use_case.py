from typing import Optional

from conduit.domain.entities.articles import ArticleWithAuthor
from conduit.domain.entities.users import User


class GetArticleBySlugUseCase:
    def __init__(self) -> None:
        pass

    async def __call__(
        self,
        slug: str,
        current_user: Optional[User],
    ) -> ArticleWithAuthor:
        raise NotImplementedError
