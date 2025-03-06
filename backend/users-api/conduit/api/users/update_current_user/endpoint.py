from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status
from returns.functions import raise_exception

from conduit.api.errors.mappers import map_application_error
from conduit.api.openapi.unauthorized_error import unauthorized_error
from conduit.api.openapi.validation_error import validation_error
from conduit.api.security.dependencies import CurrentUser, JwtToken
from conduit.api.tags import Tag
from conduit.api.users.contracts import (
    UpdateCurrentUserApiRequest,
    UserDetailsApiResponse,
)
from conduit.application.users.use_cases.update_current_user.use_case import (
    UpdateCurrentUserUseCase,
)
from conduit.containers import Container

router = APIRouter()


@router.put(
    path="/user",
    responses={
        **unauthorized_error(),
        **validation_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="Update current user details",
    tags=[Tag.Users],
)
@inject
async def update_current_user(
    jwt_token: JwtToken,
    current_user: CurrentUser,
    request: Annotated[UpdateCurrentUserApiRequest, Body()],
    update_user: UpdateCurrentUserUseCase = Depends(  # noqa: FAST002
        Provide[Container.update_current_user_use_case],
    ),
) -> UserDetailsApiResponse:
    user = await update_user(request.to_command(current_user))

    return (
        user.map(lambda u: UserDetailsApiResponse.from_user(u, jwt_token))
        .alt(map_application_error)
        .alt(raise_exception)
        .unwrap()
    )
