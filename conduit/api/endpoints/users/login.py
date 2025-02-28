from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status

from conduit.api import open_api
from conduit.api.endpoints.users.contract import (
    LoginUserApiRequest,
    UserDetailsApiResponse,
)
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.use_cases.login_user.use_case import LoginUserUseCase

router = APIRouter()


@router.post(
    path="/users/login",
    responses={
        **open_api.unauthorized_error_no_body(),
        **open_api.validation_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="Log in a user",
    tags=[Tag.Users],
)
@inject
async def login_user(
    request: Annotated[LoginUserApiRequest, Body()],
    login_user: LoginUserUseCase = Depends(Provide[Container.login_user_use_case]),
) -> UserDetailsApiResponse:
    logged_in_user = await login_user(request.to_login_details())
    return UserDetailsApiResponse.from_logged_in_user(logged_in_user)
