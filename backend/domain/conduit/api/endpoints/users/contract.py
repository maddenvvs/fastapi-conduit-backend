from typing import Optional, final

from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing_extensions import Self

from conduit.domain.entities.users import (
    LoggedInUser,
    RegisteredUser,
    RegisterUserDetails,
    User,
    UserLoginDetails,
)
from conduit.domain.use_cases.update_current_user.use_case import (
    UpdateCurrentUserRequest,
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

    def to_login_details(self) -> UserLoginDetails:
        user = self.user
        return UserLoginDetails(
            email=user.email,
            password=user.password,
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

    def to_domain(self) -> RegisterUserDetails:
        user = self.user
        return RegisterUserDetails(
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

    def to_domain(self, current_user: User) -> UpdateCurrentUserRequest:
        user = self.user

        return UpdateCurrentUserRequest(
            current_user=current_user,
            username=user.username,
            email=user.email,
            password=user.password,
            image_url=str(user.image) if user.image else None,
            bio=user.bio,
        )


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
                image=user.image,
                token=jwt_token,
            ),
        )

    @classmethod
    def from_logged_in_user(cls, user: LoggedInUser) -> Self:
        return cls(
            user=UserData(
                username=user.username,
                email=user.email,
                bio=user.bio,
                image=user.image,
                token=user.token,
            ),
        )

    @classmethod
    def from_registered_user(cls, user: RegisteredUser) -> Self:
        return cls(
            user=UserData(
                username=user.username,
                email=user.email,
                bio=user.bio,
                image=user.image,
                token=user.token,
            ),
        )
