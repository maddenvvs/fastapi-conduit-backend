from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from conduit.api import open_api
from conduit.api.endpoints.profiles.contract import ProfileDetailsApiResponse, Username
from conduit.api.security.dependencies import CurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.use_cases.follow_profile.use_case import FollowProfileUseCase

router = APIRouter()


@router.post(
    path="/profiles/{username}/follow",
    responses={
        **open_api.validation_error(),
        **open_api.not_found_error("Profile"),
    },
    status_code=status.HTTP_202_ACCEPTED,
    summary="Follow a user with a username",
    tags=[Tag.Profiles],
)
@inject
async def follow_profile_by_name(
    username: Username,
    current_user: CurrentUser,
    follow_profile: FollowProfileUseCase = Depends(  # noqa: FAST002
        Provide[Container.follow_profile_use_case],
    ),
) -> ProfileDetailsApiResponse:
    followed_profile = await follow_profile(username, current_user)
    if followed_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return ProfileDetailsApiResponse.from_profile(followed_profile)
