from fastapi import APIRouter

from conduit.api.routes import health_check, tags

router = APIRouter(prefix="/api")

router.include_router(health_check.router)
router.include_router(tags.router)
