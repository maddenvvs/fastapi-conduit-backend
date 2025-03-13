from fastapi import APIRouter

import conduit.api.endpoints.articles.create as create_article
import conduit.api.endpoints.articles.delete as articles_delete_by_slug
import conduit.api.endpoints.articles.favorite as articles_favorite
import conduit.api.endpoints.articles.feed as feed_articles
import conduit.api.endpoints.articles.get_by_slug as articles_get_by_slug
import conduit.api.endpoints.articles.list as list_articles
import conduit.api.endpoints.articles.unfavorite as articles_unfavorite
import conduit.api.endpoints.articles.update as article_update
import conduit.api.endpoints.comments.add as add_comment
import conduit.api.endpoints.comments.delete as delete_comment
import conduit.api.endpoints.comments.list as list_comments
import conduit.api.endpoints.health.get as health_get
import conduit.api.endpoints.profiles.follow as profiles_follow
import conduit.api.endpoints.profiles.get_by_username as profiles_get_by_username
import conduit.api.endpoints.profiles.unfollow as profiles_unfollow
import conduit.api.endpoints.tags.list as tags_list

router = APIRouter(prefix="/api")

router.include_router(feed_articles.router)
router.include_router(articles_get_by_slug.router)
router.include_router(article_update.router)
router.include_router(articles_favorite.router)
router.include_router(articles_unfavorite.router)
router.include_router(list_articles.router)
router.include_router(create_article.router)
router.include_router(articles_delete_by_slug.router)

router.include_router(list_comments.router)
router.include_router(add_comment.router)
router.include_router(delete_comment.router)

router.include_router(tags_list.router)

router.include_router(profiles_get_by_username.router)
router.include_router(profiles_follow.router)
router.include_router(profiles_unfollow.router)

router.include_router(health_get.router)
