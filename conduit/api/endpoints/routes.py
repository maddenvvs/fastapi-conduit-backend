from fastapi import APIRouter

import conduit.api.endpoints.articles.create as create_article
import conduit.api.endpoints.articles.list as list_articles

# import conduit.api.endpoints.articles.get_by_slug as articles_get_by_slug
import conduit.api.endpoints.health.get as health_get
import conduit.api.endpoints.profiles.get_profile_by_username as profiles_get_by_username
import conduit.api.endpoints.tags.list as tags_list
import conduit.api.endpoints.users.get_current_user as users_get_current_user
import conduit.api.endpoints.users.login as users_login
import conduit.api.endpoints.users.register as users_register
import conduit.api.endpoints.users.update_current_user as users_update_current_user

router = APIRouter(prefix="/api")

# router.include_router(articles_get_by_slug.router)
router.include_router(list_articles.router)
router.include_router(create_article.router)

router.include_router(tags_list.router)

router.include_router(users_get_current_user.router)
router.include_router(users_update_current_user.router)
router.include_router(users_register.router)
router.include_router(users_login.router)

router.include_router(profiles_get_by_username.router)

router.include_router(health_get.router)
