from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status

from conduit.api import open_api
from conduit.api.endpoints.users.contract import (
    UpdateCurrentUserApiRequest,
    UserDetailsApiResponse,
)
from conduit.api.security.dependencies import CurrentUser, JwtToken
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.use_cases.update_current_user.use_case import (
    UpdateCurrentUserUseCase,
)

router = APIRouter()


@router.put(
    path="/user",
    response_model=UserDetailsApiResponse,
    responses={
        **open_api.unauthorized_error(),
        **open_api.validation_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="Update current user details",
    tags=[Tag.Users],
)
@inject
async def update_current_user(
    jwt_token: JwtToken,
    current_user: CurrentUser,
    request: Annotated[
        UpdateCurrentUserApiRequest,
        Body(),
    ],
    update_user: UpdateCurrentUserUseCase = Depends(
        Provide[Container.update_current_user_use_case]
    ),
) -> UserDetailsApiResponse:
    updated_user = await update_user(request.to_domain(current_user))
    return UserDetailsApiResponse.from_user(updated_user, jwt_token)
