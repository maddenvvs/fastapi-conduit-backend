from typing import Annotated, Optional, final

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status
from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Self

from conduit.api import open_api
from conduit.containers import Container
from conduit.domain.entities.users import RegisteredUser, RegisterUserDetails
from conduit.domain.use_cases.register_user.use_case import RegisterUserUseCase


@final
class RegisterUserData(BaseModel):
    username: str = Field(
        description="User name used in a profile. Should be unique among other usernames.",
        examples=["walkmansit"],
        min_length=1,
    )
    email: EmailStr = Field(
        description="Email address. Should be unique among other emails.",
    )
    password: str = Field(
        description="Password to be used during the login.",
        examples=["use_your_own_password"],
        min_length=1,
    )


@final
class RegisterUserApiRequest(BaseModel):
    user: RegisterUserData = Field(description="New user information.")

    def to_domain(self) -> RegisterUserDetails:
        user = self.user
        return RegisterUserDetails(
            username=user.username,
            email=user.email,
            password=user.password,
        )


@final
class RegisteredUserData(BaseModel):
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
class RegisterUserApiResponse(BaseModel):
    user: RegisteredUserData

    @classmethod
    def from_domain(cls, user: RegisteredUser) -> Self:
        return cls(
            user=RegisteredUserData(
                username=user.username,
                email=user.email,
                bio=user.bio,
                image=user.image,
                token=user.token,
            )
        )


router = APIRouter()


@router.post(
    path="/users",
    response_model=RegisterUserApiResponse,
    responses={
        **open_api.validation_error(),
    },
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    tags=["Users"],
)
@inject
async def register_user(
    request: Annotated[
        RegisterUserApiRequest,
        Body(),
    ],
    register_user: RegisterUserUseCase = Depends(
        Provide[Container.register_user_use_case]
    ),
) -> RegisterUserApiResponse:
    registered_user = await register_user(request.to_domain())
    return RegisterUserApiResponse.from_domain(registered_user)
