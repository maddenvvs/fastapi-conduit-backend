from fastapi import APIRouter

from conduit.api.routes import articles, health_check, tags

router = APIRouter(prefix="/api")

router.include_router(health_check.router)
router.include_router(tags.router)
router.include_router(articles.router)
