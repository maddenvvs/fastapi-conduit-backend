from typing import Annotated, Optional, final

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field
from typing_extensions import Self

from conduit.api import open_api
from conduit.api.json import DateTime
from conduit.api.security.dependencies import CurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.entities.articles import BodylessArticleWithAuthor
from conduit.domain.use_cases.feed_articles.use_case import (
    FeedArticlesRequest,
    FeedArticlesResponse,
    FeedArticlesUseCase,
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
    created_at: DateTime = Field(alias="createdAt")
    updated_at: DateTime = Field(alias="updatedAt")
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
    def from_domain(cls, articles_info: FeedArticlesResponse) -> Self:
        return cls(
            articlesCount=articles_info.articles_count,
            articles=[ListedArticleData.from_domain(a) for a in articles_info.articles],
        )


router = APIRouter()


@router.get(
    path="/articles/feed",
    response_model=ListArticlesApiResponse,
    responses={
        **open_api.unauthorized_error(),
        **open_api.validation_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="Personal articles feed",
    tags=[Tag.Articles],
)
@inject
async def feed_articles(
    current_user: CurrentUser,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    use_case: FeedArticlesUseCase = Depends(Provide[Container.feed_articles_use_case]),
) -> ListArticlesApiResponse:
    articles_info = await use_case(
        FeedArticlesRequest(
            limit=limit,
            offset=offset,
            user=current_user,
        )
    )
    return ListArticlesApiResponse.from_domain(articles_info)
