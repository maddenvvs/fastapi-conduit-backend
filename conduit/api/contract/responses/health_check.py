from pydantic import BaseModel


class HealthCheckApiResponse(BaseModel):
    success: bool
    version: str
    message: str
