from fastapi import APIRouter

from conduit.api.contract.responses.health_check import HealthCheckApiResponse


router = APIRouter(
    tags=["Health Check"],
)


@router.get(
    path="/health-check",
    response_model=HealthCheckApiResponse,
)
async def health_check() -> HealthCheckApiResponse:
    return HealthCheckApiResponse(
        success=True,
        version="0.0.1",
        message="Conduit Realworld API (in FastAPI)",
    )
