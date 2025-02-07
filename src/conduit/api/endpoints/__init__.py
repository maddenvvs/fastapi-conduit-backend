from fastapi import APIRouter

import conduit.api.endpoints.articles.get_by_slug as articles_get_by_slug
import conduit.api.endpoints.health.get as health_get
import conduit.api.endpoints.tags.list as tags_list
import conduit.api.endpoints.users.login as users_login

router = APIRouter(prefix="/api")

router.include_router(articles_get_by_slug.router)
router.include_router(health_get.router)
router.include_router(tags_list.router)
router.include_router(users_login.router)
