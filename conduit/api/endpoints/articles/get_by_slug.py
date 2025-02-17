import datetime
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from conduit.containers import Container
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
    created_at: datetime.datetime = Field(alias="createdAt")
    updated_at: datetime.datetime = Field(alias="updatedAt")
    favorited: bool
    favorites_count: int = Field(alias="favoritesCount")
    author: ArticleAuthorData


class GetArticleBySlugApiResponse(BaseModel):
    article: ArticleData


router = APIRouter()


@router.get(
    path="/articles/{slug}",
    response_model=GetArticleBySlugApiResponse,
    tags=["Articles"],
)
@inject
async def get_article_by_slug(
    slug: str,
    get_article_by_slug: GetArticleBySlugUseCase = Depends(
        Provide[Container.get_article_by_slug_use_case]
    ),
) -> GetArticleBySlugApiResponse:
    raise NotImplementedError
