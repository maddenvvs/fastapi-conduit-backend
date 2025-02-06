from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from conduit.domain.repositories.articles import IArticlesRepository
from conduit.domain.repositories.tags import ITagsRepository
from conduit.domain.services.articles import ArticlesService
from conduit.domain.services.tags import TagsService
from conduit.domain.services.users.user_auth_service import UserAuthService
from conduit.persistence.repositories.articles import InMemoryArticlesRepository
from conduit.persistence.repositories.tags import InMemoryTagsRepository

_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
_session = async_sessionmaker(bind=_engine, expire_on_commit=False)


async def create_session() -> AsyncIterator[AsyncSession]:
    async with _session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


DbSession = Annotated[AsyncSession, Depends(create_session)]


async def create_tags_repository(session: DbSession) -> ITagsRepository:
    return InMemoryTagsRepository()


async def create_tags_service(
    repository: Annotated[ITagsRepository, Depends(create_tags_repository)]
) -> TagsService:
    return TagsService(repository=repository)


async def create_articles_repository() -> IArticlesRepository:
    return InMemoryArticlesRepository()


async def create_articles_service(
    repository: Annotated[IArticlesRepository, Depends(create_articles_repository)]
) -> ArticlesService:
    return ArticlesService(repository=repository)


async def create_user_auth_service() -> UserAuthService:
    return UserAuthService()


ITagsService = Annotated[TagsService, Depends(create_tags_service)]
IArticlesService = Annotated[ArticlesService, Depends(create_articles_service)]
IUserAuthService = Annotated[UserAuthService, Depends(create_user_auth_service)]
