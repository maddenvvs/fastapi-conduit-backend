from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from conduit.containers import Container
from conduit.domain.entities.users import LoggedInUser, UserLoginDetails
from conduit.domain.use_cases.login_user.use_case import LoginUserUseCase


class LoginUserDetails(BaseModel):
    email: str
    password: str


class LoginUserApiRequest(BaseModel):
    user: LoginUserDetails

    def to_login_details(self) -> UserLoginDetails:
        user = self.user
        return UserLoginDetails(
            email=user.email,
            password=user.password,
        )


class LoggedInUserData(BaseModel):
    email: str
    username: str
    bio: str
    image: Optional[str]
    token: str


class LoginUserApiResponse(BaseModel):
    user: LoggedInUserData

    @classmethod
    def from_logged_in_user(cls, user: LoggedInUser) -> "LoginUserApiResponse":
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
    tags=["Users"],
)
@inject
async def login_user(
    request: LoginUserApiRequest,
    login_user: LoginUserUseCase = Depends(Provide[Container.login_user_use_case]),
) -> LoginUserApiResponse:
    logged_in_user = await login_user(request.to_login_details())
    return LoginUserApiResponse.from_logged_in_user(logged_in_user)
