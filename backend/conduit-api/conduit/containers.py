from typing import final

from dependency_injector import containers, providers

from conduit.application.articles.services.slug_service import SlugService
from conduit.application.articles.use_cases.create_article.use_case import (
    CreateArticleUseCase,
)
from conduit.application.articles.use_cases.delete_article_by_slug.use_case import (
    DeleteArticleBySlugUseCase,
)
from conduit.application.articles.use_cases.favorite_article.use_case import (
    FavoriteArticleUseCase,
)
from conduit.application.articles.use_cases.feed_articles.use_case import (
    FeedArticlesUseCase,
)
from conduit.application.articles.use_cases.get_article_by_slug.use_case import (
    GetArticleBySlugUseCase,
)
from conduit.application.articles.use_cases.list_articles.use_case import (
    ListArticlesUseCase,
)
from conduit.application.articles.use_cases.unfavorite_article.use_case import (
    UnfavoriteArticleUseCase,
)
from conduit.application.articles.use_cases.update_article.use_case import (
    UpdateArticleUseCase,
)
from conduit.application.comments.services.comments_service import CommentsService
from conduit.application.comments.use_cases.add_comment.use_case import (
    AddCommentToArticleUseCase,
)
from conduit.application.comments.use_cases.delete_comment.use_case import (
    DeleteArticleCommentUseCase,
)
from conduit.application.comments.use_cases.list_comments.use_case import (
    ListArticleCommentsUseCase,
)
from conduit.application.common.services.articles_service import ArticlesService
from conduit.application.common.services.profiles_service import ProfilesService
from conduit.application.profiles.use_cases.follow_profile.use_case import (
    FollowProfileUseCase,
)
from conduit.application.profiles.use_cases.get_profile_by_name.use_case import (
    GetProfileByNameUseCase,
)
from conduit.application.profiles.use_cases.unfollow_profile.use_case import (
    UnfollowProfileUseCase,
)
from conduit.application.tags.services.tags_service import TagsService
from conduit.application.tags.use_cases.list_tags.use_case import ListTagsUseCase
from conduit.infrastructure.messaging.events_subscriber import RabbitMQEventsSubscriber
from conduit.infrastructure.persistence.database_seeder import Database, DatabaseSeeder
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
from conduit.settings import get_settings
from conduit.shared.api.security.auth_token_service import AuthTokenService
from conduit.shared.infrastructure.current_time import current_time
from conduit.shared.infrastructure.messaging.rabbitmq_broker import RabbitMQBroker
from conduit.shared.infrastructure.persistence.unit_of_work import (
    SqlAlchemyUnitOfWorkFactory,
)


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

    db_seeder = providers.Singleton(
        DatabaseSeeder,
        db=db,
        now=now,
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
