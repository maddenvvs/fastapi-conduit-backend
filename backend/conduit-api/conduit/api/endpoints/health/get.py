from fastapi import APIRouter
from pydantic import BaseModel

from conduit.shared.api.openapi.tags import Tag


class HealthCheckApiResponse(BaseModel):
    success: bool
    version: str
    message: str


SUCCESS_RESPONSE = HealthCheckApiResponse(
    success=True,
    version="0.0.1",
    message="Conduit Realworld API (in FastAPI)",
)

router = APIRouter()


@router.get(
    path="/health",
    tags=[Tag.Health],
)
async def health_check() -> HealthCheckApiResponse:
    return SUCCESS_RESPONSE
