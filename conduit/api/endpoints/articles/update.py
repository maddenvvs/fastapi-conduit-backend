from typing import Annotated, Optional, final

from dependency_injector.wiring import inject
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field

from conduit.api import open_api
from conduit.api.endpoints.articles.contract import (
    ArticleSlug,
    ArticleWithAuthorApiResponse,
)
from conduit.api.security.dependencies import CurrentUser
from conduit.api.tags import Tag

router = APIRouter()


@final
class UpdateArticleApiRequest(BaseModel):
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    body: Optional[str] = Field(None)


@router.put(
    path="/articles/{slug}",
    response_model=ArticleWithAuthorApiResponse,
    responses={
        **open_api.unauthorized_error(),
        **open_api.not_found_error("Article"),
        **open_api.validation_error(),
    },
    summary="Update an article",
    tags=[Tag.Articles],
)
@inject
async def update_article(
    slug: ArticleSlug,
    request: Annotated[UpdateArticleApiRequest, Body()],
    current_user: CurrentUser,
) -> ArticleWithAuthorApiResponse:
    raise HTTPException(status_code=500, detail="Not implemented")
