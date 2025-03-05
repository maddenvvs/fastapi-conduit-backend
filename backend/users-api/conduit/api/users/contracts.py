from typing import Optional, final

from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Self

from conduit.application.users.use_cases.register_user.command import (
    RegisterUserCommand,
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
