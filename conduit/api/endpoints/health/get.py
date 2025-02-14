from fastapi import APIRouter
from pydantic import BaseModel


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
    response_model=HealthCheckApiResponse,
    tags=["Health"],
)
async def health_check() -> HealthCheckApiResponse:
    return SUCCESS_RESPONSE
