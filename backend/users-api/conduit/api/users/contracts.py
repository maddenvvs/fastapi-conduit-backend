from typing import Optional, final

from pydantic import BaseModel, Field
from typing_extensions import Self

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
