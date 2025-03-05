from typing import Optional, final

from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing_extensions import Self

from conduit.application.users.use_cases.login_user.command import LoginUserCommand
from conduit.application.users.use_cases.register_user.command import (
    RegisterUserCommand,
)
from conduit.application.users.use_cases.update_current_user.command import (
    UpdateCurrentUserCommand,
)
from conduit.domain.users.user import User


@final
class UserData(BaseModel):
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
class UserDetailsApiResponse(BaseModel):
    user: UserData

    @classmethod
    def from_user(cls, user: User, jwt_token: str) -> Self:
        return cls(
            user=UserData(
                username=user.username,
                email=user.email,
                bio=user.bio,
                image=user.image_url,
                token=jwt_token,
            ),
        )


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

    def to_command(self) -> RegisterUserCommand:
        user = self.user
        return RegisterUserCommand(
            username=user.username,
            email=user.email,
            password=user.password,
        )


@final
class UpdateUserData(BaseModel):
    username: Optional[str] = Field(
        default=None,
        description="User name used in a profile. Should be unique among other usernames.",
        examples=["walkmansit"],
        min_length=1,
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="Email address. Should be unique among other emails.",
    )
    password: Optional[str] = Field(
        default=None,
        description="Password to be used during the login.",
        examples=["use_your_own_password"],
        min_length=1,
    )
    bio: Optional[str] = Field(
        default=None,
        description="The biography information of the registered user (empty by default).",
        examples=[""],
    )
    image: Optional[HttpUrl] = Field(
        default=None,
        description="The image URL of the registered user (null by default).",
        examples=[None],
    )


@final
class UpdateCurrentUserApiRequest(BaseModel):
    user: UpdateUserData = Field(description="User information to update.")

    def to_command(self, current_user: User) -> UpdateCurrentUserCommand:
        user = self.user

        return UpdateCurrentUserCommand(
            current_user=current_user,
            username=user.username,
            email=user.email,
            password=user.password,
            image_url=str(user.image) if user.image else None,
            bio=user.bio,
        )


@final
class LoginUserData(BaseModel):
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
    user: LoginUserData = Field(description="User login details.")

    def to_command(self) -> LoginUserCommand:
        user = self.user
        return LoginUserCommand(
            email=user.email,
            password=user.password,
        )
