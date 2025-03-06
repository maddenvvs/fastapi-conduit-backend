from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from conduit.api.openapi.unauthorized_error import unauthorized_error
from conduit.api.security.dependencies import CurrentUser, JwtToken
from conduit.api.tags import Tag
from conduit.api.users.contracts import UserDetailsApiResponse
from conduit.application.users.use_cases.get_current_user.use_case import (
    GetCurrentUserUseCase,
)
from conduit.containers import Container

router = APIRouter()


@router.get(
    path="/user",
    responses={
        **unauthorized_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="Get current user details",
    tags=[Tag.Users],
)
@inject
async def get_current_user(
    jwt_token: JwtToken,
    current_user: CurrentUser,
    use_case: GetCurrentUserUseCase = Depends(  # noqa: FAST002
        Provide[Container.get_current_user_use_case],
    ),
) -> UserDetailsApiResponse:
    current_user_details = await use_case(current_user)
    return UserDetailsApiResponse.from_user(current_user_details, jwt_token)
