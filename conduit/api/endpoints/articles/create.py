import datetime
from typing import Annotated, Optional, final

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status
from pydantic import BaseModel, Field
from typing_extensions import Self

from conduit.api import open_api
from conduit.api.security.dependencies import CurrentUser
from conduit.containers import Container
from conduit.domain.entities.articles import ArticleWithAuthor, NewArticleDetails
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


@final
class ArticleAuthorData(BaseModel):
    username: str
    bio: str
    image: Optional[str]
    following: bool


@final
class CreatedArticleData(BaseModel):
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
    article: CreatedArticleData

    @classmethod
    def from_domain(cls, article: ArticleWithAuthor) -> Self:
        author = article.author

        return cls(
            article=CreatedArticleData(
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


@router.post(
    path="/articles",
    response_model=CreateArticleApiResponse,
    responses={
        **open_api.unauthorized_error(),
        **open_api.validation_error(),
    },
    status_code=status.HTTP_201_CREATED,
    summary="Create a new article",
    tags=["Articles"],
)
@inject
async def create_article(
    new_article: Annotated[CreateArticleApiRequest, Body()],
    current_user: CurrentUser,
    create_article: CreateArticleUseCase = Depends(
        Provide[Container.create_article_use_case]
    ),
) -> CreateArticleApiResponse:
    created_article = await create_article(new_article.to_domain(), current_user.id)
    return CreateArticleApiResponse.from_domain(created_article)
