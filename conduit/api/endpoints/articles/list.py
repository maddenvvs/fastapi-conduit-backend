import datetime
from typing import Annotated, Optional, final

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field
from typing_extensions import Self

from conduit.api import open_api
from conduit.api.security.dependencies import OptionalCurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.entities.articles import BodylessArticleWithAuthor
from conduit.domain.use_cases.list_articles.use_case import (
    ListArticlesRequest,
    ListArticlesResponse,
    ListArticlesUseCase,
)


@final
class ArticleAuthorData(BaseModel):
    username: str
    bio: str
    image: Optional[str]
    following: bool


@final
class ListedArticleData(BaseModel):
    slug: str
    title: str
    description: str
    tags: list[str] = Field(alias="tagList")
    created_at: datetime.datetime = Field(alias="createdAt")
    updated_at: datetime.datetime = Field(alias="updatedAt")
    favorited: bool
    favorites_count: int = Field(alias="favoritesCount")
    author: ArticleAuthorData

    @classmethod
    def from_domain(cls, article: BodylessArticleWithAuthor) -> Self:
        author = article.author

        return cls(
            slug=article.slug,
            title=article.title,
            description=article.description,
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


@final
class ListArticlesApiResponse(BaseModel):
    articles: list[ListedArticleData]
    articles_count: int = Field(alias="articlesCount")

    @classmethod
    def from_domain(cls, articles_info: ListArticlesResponse) -> Self:
        return cls(
            articlesCount=articles_info.articles_count,
            articles=[ListedArticleData.from_domain(a) for a in articles_info.articles],
        )


router = APIRouter()


@router.get(
    path="/articles",
    response_model=ListArticlesApiResponse,
    responses={
        **open_api.unauthorized_error(),
        **open_api.validation_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="List all articles",
    tags=[Tag.Articles],
)
@inject
async def list_articles(
    optional_user: OptionalCurrentUser,
    limit: Annotated[int, Query(ge=1, le=20)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    use_case: ListArticlesUseCase = Depends(Provide[Container.list_articles_use_case]),
) -> ListArticlesApiResponse:
    articles_info = await use_case(
        ListArticlesRequest(limit=limit, offset=offset, user=optional_user)
    )
    return ListArticlesApiResponse.from_domain(articles_info)
