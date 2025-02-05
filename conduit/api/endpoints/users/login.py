from fastapi import APIRouter
from pydantic import BaseModel

from conduit.api.dependencies import IUserAuthService
from conduit.domain.entities.users import LoggedInUser, UserLoginDetails


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
    image: str
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
async def login_user(
    request: LoginUserApiRequest,
    user_auth_service: IUserAuthService,
) -> LoginUserApiResponse:
    logged_in_user = await user_auth_service.login_user(request.to_login_details())
    return LoginUserApiResponse.from_logged_in_user(logged_in_user)
