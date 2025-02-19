from typing import Annotated, Optional, final

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from typing_extensions import Self

from conduit.api import open_api
from conduit.api.security.dependencies import OptionalCurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.entities.profiles import Profile
from conduit.domain.use_cases.get_profile_by_name.use_case import (
    GetProfileByNameUseCase,
)


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
class GetProfileByNameApiResponse(BaseModel):
    user: ProfileData

    @classmethod
    def from_domain(cls, profile: Profile) -> Self:
        return cls(
            user=ProfileData(
                username=profile.username,
                bio=profile.bio,
                image=profile.image,
                following=profile.following,
            )
        )


router = APIRouter()


@router.get(
    path="/profiles/{username}",
    response_model=GetProfileByNameApiResponse,
    responses={
        **open_api.not_found_error("Profile"),
        **open_api.validation_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="Get profile details by username",
    tags=[Tag.Profiles],
)
@inject
async def get_profile_by_username(
    username: Annotated[str, Path(description="Username of a registered user.")],
    optional_user: OptionalCurrentUser,
    get_profile_by_name: GetProfileByNameUseCase = Depends(
        Provide[Container.get_profile_by_name_use_case]
    ),
) -> GetProfileByNameApiResponse:
    profile_details = await get_profile_by_name(username, optional_user)
    if profile_details is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile is not found.",
        )

    return GetProfileByNameApiResponse.from_domain(profile_details)
