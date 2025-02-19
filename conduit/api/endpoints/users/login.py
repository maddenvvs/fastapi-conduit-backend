from typing import Annotated, Optional, final

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status
from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Self

from conduit.api import open_api
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.entities.users import LoggedInUser, UserLoginDetails
from conduit.domain.use_cases.login_user.use_case import LoginUserUseCase


@final
class LoginUserDetails(BaseModel):
    email: EmailStr = Field(
        description="Email address used during the registration.",
    )
    password: str = Field(
        description="Password provided during the registration.",
        examples=["use_your_own_password"],
        min_length=1,
    )


@final
class LoginUserApiRequest(BaseModel):
    user: LoginUserDetails = Field(description="User login details.")

    def to_login_details(self) -> UserLoginDetails:
        user = self.user
        return UserLoginDetails(
            email=user.email,
            password=user.password,
        )


@final
class LoggedInUserData(BaseModel):
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
    )
    image: Optional[str] = Field(
        description="The image URL of the logged in user.",
    )
    token: str = Field(
        description="JSON Web Token (JWT) issued for the logged in user.",
        examples=["header.payload.signature"],
    )


@final
class LoginUserApiResponse(BaseModel):
    user: LoggedInUserData

    @classmethod
    def from_logged_in_user(cls, user: LoggedInUser) -> Self:
        return cls(
            user=LoggedInUserData(
                username=user.username,
                email=user.email,
                bio=user.bio,
                image=user.image,
                token=user.token,
            )
        )


router = APIRouter()


@router.post(
    path="/users/login",
    response_model=LoginUserApiResponse,
    responses={
        **open_api.validation_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="Log in a user",
    tags=[Tag.Users],
)
@inject
async def login_user(
    request: Annotated[LoginUserApiRequest, Body()],
    login_user: LoginUserUseCase = Depends(Provide[Container.login_user_use_case]),
) -> LoginUserApiResponse:
    logged_in_user = await login_user(request.to_login_details())
    return LoginUserApiResponse.from_logged_in_user(logged_in_user)
