import datetime
from typing import Optional

from conduit.domain.entities.articles import Article, ArticleAuthor
from conduit.domain.repositories.articles import IArticlesRepository


class InMemoryArticlesRepository(IArticlesRepository):

    async def find_article_by_slug(self, slug: str) -> Optional[Article]:
        if slug == "how-to-train-your-dragon":
            return Article(
                slug="how-to-train-your-dragon",
                title="How to train your dragon",
                description="Ever wonder how?",
                body="It takes a Jacobian",
                tags=["dragons", "training"],
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
                favorited=False,
                favorites_count=0,
                author=ArticleAuthor(
                    username="jake",
                    bio="I work at statefarm",
                    image="https://i.stack.imgur.com/xHWG8.jpg",
                    following=False,
                ),
            )
        return None
