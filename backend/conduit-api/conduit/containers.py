from typing import final

from dependency_injector import containers, providers

from conduit.domain.services.articles_service import ArticlesService
from conduit.domain.services.auth_token_service import AuthTokenService
from conduit.domain.services.comments_service import CommentsService
from conduit.domain.services.profiles_service import ProfilesService
from conduit.domain.services.slug_service import SlugService
from conduit.domain.services.tags_service import TagsService
from conduit.domain.use_cases.add_comment.use_case import AddCommentToArticleUseCase
from conduit.domain.use_cases.create_article.use_case import CreateArticleUseCase
from conduit.domain.use_cases.delete_article_by_slug.use_case import (
    DeleteArticleBySlugUseCase,
)
from conduit.domain.use_cases.delete_comment.use_case import DeleteArticleCommentUseCase
from conduit.domain.use_cases.favorite_article.use_case import FavoriteArticleUseCase
from conduit.domain.use_cases.feed_articles.use_case import FeedArticlesUseCase
from conduit.domain.use_cases.follow_profile.use_case import FollowProfileUseCase
from conduit.domain.use_cases.get_article_by_slug.use_case import (
    GetArticleBySlugUseCase,
)
from conduit.domain.use_cases.get_profile_by_name.use_case import (
    GetProfileByNameUseCase,
)
from conduit.domain.use_cases.list_articles.use_case import ListArticlesUseCase
from conduit.domain.use_cases.list_comments.use_case import ListArticleCommentsUseCase
from conduit.domain.use_cases.list_tags.use_case import ListTagsUseCase
from conduit.domain.use_cases.unfavorite_article.use_case import (
    UnfavoriteArticleUseCase,
)
from conduit.domain.use_cases.unfollow_profile.use_case import UnfollowProfileUseCase
from conduit.domain.use_cases.update_article.use_case import UpdateArticleUseCase
from conduit.infrastructure.current_time import current_time
from conduit.infrastructure.messaging.events_subscriber import RabbitMQEventsSubscriber
from conduit.infrastructure.messaging.rabbitmq_broker import RabbitMQBroker
from conduit.infrastructure.persistence.database import Database
from conduit.infrastructure.persistence.repositories.articles import (
    SQLiteArticlesRepository,
)
from conduit.infrastructure.persistence.repositories.comments import (
    SQLiteCommentsRepository,
)
from conduit.infrastructure.persistence.repositories.favorites import (
    SQLiteFavoritesRepository,
)
from conduit.infrastructure.persistence.repositories.followers import (
    SQLiteFollowersRepository,
)
from conduit.infrastructure.persistence.repositories.tags import SQLiteTagsRepository
from conduit.infrastructure.persistence.repositories.users import SQLiteUsersRepository
from conduit.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWorkFactory
from conduit.settings import get_settings


@final
class Container(containers.DeclarativeContainer):
    __self__: providers.Self["Container"] = providers.Self()

    wiring_config = containers.WiringConfiguration(packages=[".api"])

    app_settings = providers.Singleton(get_settings)

    db = providers.Singleton(
        Database,
        db_url=app_settings.provided.database_url,
    )

    uow_factory = providers.Factory(
        SqlAlchemyUnitOfWorkFactory,
        db=db,
    )

    now = providers.Object(current_time)

    slug_service = providers.Singleton(SlugService)

    message_broker = providers.Singleton(
        RabbitMQBroker,
        rabbitmq_url=app_settings.provided.rabbitmq_url,
    )

    # Repositories

    tags_repository = providers.Factory(
        SQLiteTagsRepository,
        now=now,
    )

    users_repository = providers.Factory(
        SQLiteUsersRepository,
        now=now,
    )

    followers_repository = providers.Factory(
        SQLiteFollowersRepository,
        now=now,
    )

    articles_repository = providers.Factory(
        SQLiteArticlesRepository,
        now=now,
    )

    favorites_repository = providers.Factory(
        SQLiteFavoritesRepository,
        now=now,
    )

    comments_repository = providers.Factory(
        SQLiteCommentsRepository,
        now=now,
    )

    # Services

    tags_service = providers.Factory(
        TagsService,
        tags_repository=tags_repository,
    )

    auth_token_service = providers.Factory(
        AuthTokenService,
        secret_key=app_settings.provided.jwt_secret_key,
        algorithm=app_settings.provided.jwt_algorithm,
        token_expiration_minutes=app_settings.provided.jwt_token_expiration_minutes,
    )

    profiles_service = providers.Factory(
        ProfilesService,
        users_repository=users_repository,
        followers_repository=followers_repository,
    )

    articles_service = providers.Factory(
        ArticlesService,
        articles_repository=articles_repository,
        tags_repository=tags_repository,
        profiles_service=profiles_service,
        favorites_repository=favorites_repository,
        slug_service=slug_service,
    )

    comments_service = providers.Factory(
        CommentsService,
        comments_repository=comments_repository,
        articles_service=articles_service,
        profiles_service=profiles_service,
    )

    # Use cases

    list_tags_use_case = providers.Factory(
        ListTagsUseCase,
        uow_factory=uow_factory,
        tags_service=tags_service,
    )

    get_article_by_slug_use_case = providers.Factory(
        GetArticleBySlugUseCase,
        uow_factory=uow_factory,
        articles_service=articles_service,
    )

    create_article_use_case = providers.Factory(
        CreateArticleUseCase,
        uow_factory=uow_factory,
        articles_service=articles_service,
    )

    list_articles_use_case = providers.Factory(
        ListArticlesUseCase,
        uow_factory=uow_factory,
        articles_repository=articles_repository,
    )

    feed_articles_use_case = providers.Factory(
        FeedArticlesUseCase,
        uow_factory=uow_factory,
        articles_repository=articles_repository,
    )

    get_profile_by_name_use_case = providers.Factory(
        GetProfileByNameUseCase,
        uow_factory=uow_factory,
        profiles_service=profiles_service,
    )

    follow_profile_use_case = providers.Factory(
        FollowProfileUseCase,
        uow_factory=uow_factory,
        profiles_service=profiles_service,
    )

    unfollow_profile_use_case = providers.Factory(
        UnfollowProfileUseCase,
        uow_factory=uow_factory,
        profiles_service=profiles_service,
    )

    favorite_article_use_case = providers.Factory(
        FavoriteArticleUseCase,
        uow_factory=uow_factory,
        articles_service=articles_service,
    )

    unfavorite_article_use_case = providers.Factory(
        UnfavoriteArticleUseCase,
        uow_factory=uow_factory,
        articles_service=articles_service,
    )

    delete_article_by_slug_use_case = providers.Factory(
        DeleteArticleBySlugUseCase,
        uow_factory=uow_factory,
        articles_service=articles_service,
    )

    update_article_use_case = providers.Factory(
        UpdateArticleUseCase,
        uow_factory=uow_factory,
        articles_service=articles_service,
    )

    add_comment_to_article_use_case = providers.Factory(
        AddCommentToArticleUseCase,
        uow_factory=uow_factory,
        comments_service=comments_service,
    )

    list_article_comments_use_case = providers.Factory(
        ListArticleCommentsUseCase,
        uow_factory=uow_factory,
        comments_service=comments_service,
    )

    delete_article_comment_use_case = providers.Factory(
        DeleteArticleCommentUseCase,
        uow_factory=uow_factory,
        comments_service=comments_service,
    )

    events_subscriber = providers.Factory(
        RabbitMQEventsSubscriber,
        message_broker=message_broker,
        uow_factory=uow_factory,
        now=now,
    )
