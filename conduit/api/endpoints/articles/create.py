import datetime
from typing import Optional, final

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from conduit.containers import Container
from conduit.domain.use_cases.create_article.use_case import CreateArticleUseCase


@final
class NewArticleData(BaseModel):
    title: str
    description: str
    body: str
    tags: list[str] = Field(default_factory=list, alias="tagList")


@final
class CreateArticleApiRequest(BaseModel):
    article: NewArticleData


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
    tags: list[str] = Field(alias="tagList")
    created_at: datetime.datetime = Field(alias="createdAt")
    updated_at: datetime.datetime = Field(alias="updatedAt")
    favorited: bool
    favorites_count: int = Field(alias="favoritesCount")
    author: ArticleAuthorData


@final
class CreateArticleApiResponse(BaseModel):
    article: ArticleData


router = APIRouter()


@router.post(
    path="/articles",
    response_model=CreateArticleApiResponse,
    tags=["Articles"],
)
@inject
async def create_article(
    new_article: CreateArticleApiRequest,
    create_article: CreateArticleUseCase = Depends(
        Provide[Container.create_article_use_case]
    ),
) -> CreateArticleApiResponse:
    raise NotImplementedError
