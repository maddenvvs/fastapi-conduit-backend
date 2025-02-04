from pydantic import BaseModel


class GetAllTagsApiResponse(BaseModel):
    tags: list[str]
