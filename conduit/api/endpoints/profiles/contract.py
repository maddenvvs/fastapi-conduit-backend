from typing import Annotated, Optional, final

from fastapi import Path
from pydantic import BaseModel, Field
from typing_extensions import Self, TypeAlias

from conduit.domain.entities.profiles import Profile

Username: TypeAlias = Annotated[
    str,
    Path(
        description="Username of a registered user.",
    ),
]


@final
class ProfileData(BaseModel):
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
    following: bool = Field(
        description="Do I follow the user with the given username?",
        examples=[True],
    )


@final
class ProfileDetailsApiResponse(BaseModel):
    profile: ProfileData

    @classmethod
    def from_profile(cls, profile: Profile) -> Self:
        return cls(
            profile=ProfileData(
                username=profile.username,
                bio=profile.bio,
                image=profile.image,
                following=profile.following,
            )
        )
