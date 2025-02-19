from typing import Annotated, Optional, final

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status
from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Self

from conduit.api import open_api
from conduit.api.security.dependencies import CurrentUser, JwtToken
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.entities.users import User
from conduit.domain.use_cases.update_current_user.use_case import (
    UpdateCurrentUserRequest,
    UpdateCurrentUserUseCase,
)


@final
class UpdateUserData(BaseModel):
    username: Optional[str] = Field(
        default=None,
        description="User name used in a profile. Should be unique among other usernames.",
        examples=["walkmansit"],
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="Email address. Should be unique among other emails.",
    )
    password: Optional[str] = Field(
        default=None,
        description="Password to be used during the login.",
        examples=["use_your_own_password"],
    )
    bio: Optional[str] = Field(
        default=None,
        description="The biography information of the registered user (empty by default).",
        examples=[""],
    )
    image: Optional[str] = Field(
        default=None,
        description="The image URL of the registered user (null by default).",
        examples=[None],
    )


@final
class UpdateCurrentUserApiRequest(BaseModel):
    user: UpdateUserData = Field(description="User information to update.")

    def to_domain(self, current_user: User) -> UpdateCurrentUserRequest:
        user = self.user

        return UpdateCurrentUserRequest(
            current_user=current_user,
            username=user.username,
            email=user.email,
            password=user.password,
            image_url=user.image,
            bio=user.bio,
        )


@final
class UpdatedUserData(BaseModel):
    email: str = Field(
        description="The email address of the registered user.",
        examples=["user@example.com"],
    )
    username: str = Field(
        description="The username of the registered user.",
        examples=["walkmansit"],
    )
    bio: str = Field(
        description="The biography information of the registered user (empty by default).",
        examples=[""],
    )
    image: Optional[str] = Field(
        description="The image URL of the registered user (null by default).",
        examples=[None],
    )
    token: str = Field(
        description="JSON Web Token (JWT) issued for the registered user.",
        examples=["header.payload.signature"],
    )


@final
class UpdateCurrentUserApiResponse(BaseModel):
    user: UpdatedUserData

    @classmethod
    def from_domain(cls, user: User, jwt_token: str) -> Self:
        return cls(
            user=UpdatedUserData(
                username=user.username,
                email=user.email,
                bio=user.bio,
                image=user.image,
                token=jwt_token,
            )
        )


router = APIRouter()


@router.put(
    path="/user",
    response_model=UpdateCurrentUserApiResponse,
    responses={
        **open_api.unauthorized_error(),
        **open_api.validation_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="Update current user details",
    tags=[Tag.Users],
)
@inject
async def update_current_user(
    jwt_token: JwtToken,
    current_user: CurrentUser,
    request: Annotated[
        UpdateCurrentUserApiRequest,
        Body(),
    ],
    update_user: UpdateCurrentUserUseCase = Depends(
        Provide[Container.update_current_user_use_case]
    ),
) -> UpdateCurrentUserApiResponse:
    updated_user = await update_user(request.to_domain(current_user))
    return UpdateCurrentUserApiResponse.from_domain(updated_user, jwt_token)
