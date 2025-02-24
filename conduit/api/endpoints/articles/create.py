from typing import Annotated, final

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status
from pydantic import BaseModel, Field

from conduit.api import open_api
from conduit.api.endpoints.articles.contract import ArticleWithAuthorApiResponse
from conduit.api.security.dependencies import CurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.entities.articles import NewArticleDetails
from conduit.domain.use_cases.create_article.use_case import CreateArticleUseCase


@final
class NewArticleData(BaseModel):
    title: str = Field(
        description="The title of the article.",
        examples=["How to write code?"],
        min_length=1,
    )
    description: str = Field(
        description="A couple of sentences what the article is about.",
        examples=["This article shows you best practices about how to write code."],
        min_length=1,
    )
    body: str = Field(
        description="The actual content of the article.",
        examples=["Very long article body..."],
        min_length=1,
    )
    tags: set[str] = Field(
        description="Optional list of tags this article belongs to.",
        examples=[["refactoring", "best_practices"]],
        default_factory=set,
        alias="tagList",
    )


@final
class CreateArticleApiRequest(BaseModel):
    article: NewArticleData

    def to_domain(self) -> NewArticleDetails:
        article = self.article

        return NewArticleDetails(
            title=article.title,
            description=article.description,
            body=article.body,
            tags=list(article.tags),
        )


router = APIRouter()


@router.post(
    path="/articles",
    response_model=ArticleWithAuthorApiResponse,
    responses={
        **open_api.unauthorized_error(),
        **open_api.validation_error(),
    },
    status_code=status.HTTP_201_CREATED,
    summary="Create a new article",
    tags=[Tag.Articles],
)
@inject
async def create_article(
    new_article: Annotated[CreateArticleApiRequest, Body()],
    current_user: CurrentUser,
    create_article: CreateArticleUseCase = Depends(
        Provide[Container.create_article_use_case]
    ),
) -> ArticleWithAuthorApiResponse:
    created_article = await create_article(new_article.to_domain(), current_user.id)
    return ArticleWithAuthorApiResponse.from_domain(created_article)
