from typing import Annotated, Optional, final

from fastapi import Path
from pydantic import BaseModel, Field
from typing_extensions import Self, TypeAlias

from conduit.api.json import DateTime
from conduit.domain.entities.articles import ArticleWithAuthor

ArticleSlug: TypeAlias = Annotated[
    str,
    Path(
        description="Article slug generated after creation",
    ),
]


@final
class ArticleAuthorData(BaseModel):
    username: str
    bio: str
    image: Optional[str]
    following: bool


@final
class ArticleData(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tag_list: list[str] = Field(alias="tagList")
    created_at: DateTime = Field(alias="createdAt")
    updated_at: DateTime = Field(alias="updatedAt")
    favorited: bool
    favorites_count: int = Field(alias="favoritesCount")
    author: ArticleAuthorData


@final
class ArticleWithAuthorApiResponse(BaseModel):
    article: ArticleData

    @classmethod
    def from_domain(cls, article: ArticleWithAuthor) -> Self:
        author = article.author

        return cls(
            article=ArticleData(
                slug=article.slug,
                title=article.title,
                description=article.description,
                body=article.body,
                tagList=article.tags,
                createdAt=article.created_at,
                updatedAt=article.updated_at,
                favorited=article.favorited,
                favoritesCount=article.favorites_count,
                author=ArticleAuthorData(
                    username=author.username,
                    bio=author.bio,
                    image=author.image,
                    following=author.following,
                ),
            )
        )
