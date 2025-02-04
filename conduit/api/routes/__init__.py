from fastapi import APIRouter

from conduit.api.routes import health_check

router = APIRouter(prefix="/api")

router.include_router(health_check.router)
