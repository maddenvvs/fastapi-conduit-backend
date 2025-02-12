from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from conduit.containers import Container
from conduit.domain.entities.users import RegisteredUser, RegisterUserDetails
from conduit.domain.use_cases.register_user import RegisterUserUseCase


class RegisterUserData(BaseModel):
    username: str
    email: str
    password: str


class RegisterUserApiRequest(BaseModel):
    user: RegisterUserData

    def to_domain(self) -> RegisterUserDetails:
        user = self.user
        return RegisterUserDetails(
            username=user.username,
            email=user.email,
            password=user.password,
        )


class RegisteredUserData(BaseModel):
    email: str
    username: str
    bio: str
    image: Optional[str]
    token: str


class RegisterUserApiResponse(BaseModel):
    user: RegisteredUserData

    @classmethod
    def from_domain(cls, user: RegisteredUser) -> "RegisterUserApiResponse":
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
    tags=["Users"],
)
@inject
async def login_user(
    request: RegisterUserApiRequest,
    register_user: RegisterUserUseCase = Depends(
        Provide[Container.register_user_use_case]
    ),
) -> RegisterUserApiResponse:
    registered_user = await register_user(request.to_domain())
    return RegisterUserApiResponse.from_domain(registered_user)
