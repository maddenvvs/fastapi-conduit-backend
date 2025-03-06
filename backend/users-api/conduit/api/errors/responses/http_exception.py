from typing import final

from pydantic import BaseModel, Field


@final
class HttpExceptionApiResponse(BaseModel):
    detail: str = Field(
        description="Detailed error message.",
        examples=["Missing authorization credentials"],
    )
