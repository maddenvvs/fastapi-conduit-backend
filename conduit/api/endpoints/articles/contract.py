from typing import Annotated, Optional, final

from fastapi import Path
from pydantic import BaseModel, Field
from typing_extensions import Self, TypeAlias

from conduit.api.json import DateTime
from conduit.domain.entities.articles import (
    ArticleWithAuthor,
    BodylessArticleWithAuthor,
    NewArticleDetails,
)
from conduit.domain.use_cases.feed_articles.use_case import FeedArticlesResponse
from conduit.domain.use_cases.list_articles.use_case import ListArticlesResponse

ArticleSlug: TypeAlias = Annotated[
    str,
    Path(
        description="Article slug generated after creation",
        min_length=1,
    ),
]


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


@final
class ArticleWithAuthorApiResponse(BaseModel):
    article: ArticleData

    @classmethod
    def from_article_with_author(cls, article: ArticleWithAuthor) -> Self:
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


@final
class BodylessArticleData(BaseModel):
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
    def from_bodyless_article(cls, article: BodylessArticleWithAuthor) -> Self:
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
    articles: list[BodylessArticleData]
    articles_count: int = Field(alias="articlesCount")

    @classmethod
    def from_articles_info(cls, articles_info: ListArticlesResponse) -> Self:
        return cls(
            articlesCount=articles_info.articles_count,
            articles=[
                BodylessArticleData.from_bodyless_article(a)
                for a in articles_info.articles
            ],
        )

    @classmethod
    def from_feed_info(cls, feed_info: FeedArticlesResponse) -> Self:
        return cls(
            articlesCount=feed_info.articles_count,
            articles=[
                BodylessArticleData.from_bodyless_article(a) for a in feed_info.articles
            ],
        )
