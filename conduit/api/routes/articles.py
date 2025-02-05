from fastapi import APIRouter, status
from fastapi.responses import Response

from conduit.api.contract.responses.articles import (
    ArticleAuthorData,
    ArticleData,
    GetArticleBySlugApiResponse,
)
from conduit.api.dependencies import IArticlesService

router = APIRouter(
    prefix="/articles",
    tags=["Articles"],
)


@router.get(
    path="/{slug}",
    response_model=GetArticleBySlugApiResponse,
    responses={
        404: {},
    },
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
