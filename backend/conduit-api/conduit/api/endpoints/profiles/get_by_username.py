from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from conduit.api.endpoints.profiles.contract import ProfileDetailsApiResponse, Username
from conduit.api.security.dependencies import OptionalCurrentUser
from conduit.application.profiles.use_cases.get_profile_by_name.use_case import (
    GetProfileByNameUseCase,
)
from conduit.containers import Container
from conduit.shared.api.openapi.not_found_error import not_found_error
from conduit.shared.api.openapi.tags import Tag
from conduit.shared.api.openapi.validation_error import validation_error

router = APIRouter()


@router.get(
    path="/profiles/{username}",
    responses={
        **validation_error(),
        **not_found_error("Profile"),
    },
    status_code=status.HTTP_200_OK,
    summary="Get profile details by username",
    tags=[Tag.Profiles],
)
@inject
async def get_profile_by_username(
    username: Username,
    optional_user: OptionalCurrentUser,
    get_profile_by_name: GetProfileByNameUseCase = Depends(  # noqa: FAST002
        Provide[Container.get_profile_by_name_use_case],
    ),
) -> ProfileDetailsApiResponse:
    profile_details = await get_profile_by_name(username, optional_user)
    if profile_details is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )

    return ProfileDetailsApiResponse.from_profile(profile_details)
