from typing import Optional, final

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from typing_extensions import Self

from conduit.api import open_api
from conduit.api.security.dependencies import CurrentUser, JwtToken
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.entities.users import User
from conduit.domain.use_cases.get_current_user.use_case import GetCurrentUserUseCase


@final
class CurrentUserData(BaseModel):
    email: str = Field(
        description="The email address of the logged in user.",
        examples=["user@example.com"],
    )
    username: str = Field(
        description="The username of the logged in user.",
        examples=["walkmansit"],
    )
    bio: str = Field(
        description="The biography information of the logged in user.",
        examples=["Full-time Open Source contributor."],
    )
    image: Optional[str] = Field(
        description="The image URL of the logged in user.",
        examples=[None],
    )
    token: str = Field(
        description="JSON Web Token (JWT) issued for the logged in user.",
        examples=["header.payload.signature"],
    )


@final
class GetCurrentUserApiResponse(BaseModel):
    user: CurrentUserData

    @classmethod
    def from_domain(cls, user: User, jwt_token: str) -> Self:
        return cls(
            user=CurrentUserData(
                username=user.username,
                email=user.email,
                bio=user.bio,
                image=user.image,
                token=jwt_token,
            )
        )


router = APIRouter()


@router.get(
    path="/user",
    response_model=GetCurrentUserApiResponse,
    responses={
        **open_api.unauthorized_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="Get current user details",
    tags=[Tag.Users],
)
@inject
async def get_current_user(
    jwt_token: JwtToken,
    current_user: CurrentUser,
    use_case: GetCurrentUserUseCase = Depends(
        Provide[Container.get_current_user_use_case]
    ),
) -> GetCurrentUserApiResponse:
    current_user_details = await use_case(current_user)
    return GetCurrentUserApiResponse.from_domain(current_user_details, jwt_token)
