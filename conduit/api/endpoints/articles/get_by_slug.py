import datetime

from fastapi import APIRouter, status
from fastapi.responses import Response
from pydantic import BaseModel, Field

from conduit.api.dependencies import IArticlesService


class ArticleAuthorData(BaseModel):
    username: str
    bio: str
    image: str
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
    responses={
        404: {},
    },
    tags=["Articles"],
)
async def get_article_by_slug(
    slug: str,
    articles_service: IArticlesService,
):
    article = await articles_service.find_article_by_slug(slug)

    if article is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    author = article.author
    return GetArticleBySlugApiResponse(
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
