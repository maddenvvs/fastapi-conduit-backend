from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from conduit.api.endpoints.profiles.contract import ProfileDetailsApiResponse, Username
from conduit.api.security.dependencies import CurrentUser
from conduit.application.profiles.use_cases.follow_profile.use_case import (
    FollowProfileUseCase,
)
from conduit.containers import Container
from conduit.shared.api.openapi.not_found_error import not_found_error
from conduit.shared.api.openapi.tags import Tag
from conduit.shared.api.openapi.validation_error import validation_error

router = APIRouter()


@router.post(
    path="/profiles/{username}/follow",
    responses={
        **validation_error(),
        **not_found_error("Profile"),
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
