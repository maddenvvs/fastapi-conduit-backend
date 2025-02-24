from typing import Annotated, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from typing_extensions import Self

from conduit.api import open_api
from conduit.api.json import DateTime
from conduit.api.security.dependencies import OptionalCurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.entities.articles import ArticleWithAuthor
from conduit.domain.use_cases.get_article_by_slug.use_case import (
    GetArticleBySlugUseCase,
)


class ArticleAuthorData(BaseModel):
    username: str
    bio: str
    image: Optional[str]
    following: bool


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


class GetArticleBySlugApiResponse(BaseModel):
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


router = APIRouter()


@router.get(
    path="/articles/{slug}",
    response_model=GetArticleBySlugApiResponse,
    responses={
        **open_api.unauthorized_error(),
        **open_api.not_found_error("Article"),
    },
    summary="Get article by slug",
    tags=[Tag.Articles],
)
@inject
async def get_article_by_slug(
    slug: Annotated[str, Path(description="Article slug generated after creation")],
    optional_user: OptionalCurrentUser,
    get_article_by_slug: GetArticleBySlugUseCase = Depends(
        Provide[Container.get_article_by_slug_use_case]
    ),
) -> GetArticleBySlugApiResponse:
    article = await get_article_by_slug(slug, optional_user)
    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )

    return GetArticleBySlugApiResponse.from_domain(article)
