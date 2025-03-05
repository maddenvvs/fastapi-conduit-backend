from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException, status
from returns.functions import raise_exception

from conduit.api import open_api
from conduit.api.security.auth_token_service import AuthTokenService
from conduit.api.tags import Tag
from conduit.api.users.contracts import RegisterUserApiRequest, UserDetailsApiResponse
from conduit.application.common.errors import ApplicationError
from conduit.application.users.use_cases.register_user.use_case import (
    RegisterUserUseCase,
)
from conduit.containers import Container

router = APIRouter()


def _convert_error(exc: Exception) -> HTTPException:
    if isinstance(exc, ApplicationError):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.message,
        )

    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid request",
    )


@router.post(
    path="/users",
    responses={
        **open_api.validation_error(),
    },
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    tags=[Tag.Users],
)
@inject
async def register_user(
    request: Annotated[RegisterUserApiRequest, Body()],
    register_user: RegisterUserUseCase = Depends(  # noqa: FAST002
        Provide[Container.register_user_use_case],
    ),
    token_service: AuthTokenService = Depends(Provide[Container.auth_token_service]),  # noqa: FAST002
) -> UserDetailsApiResponse:
    registered_user = (
        (await register_user(request.to_command()))
        .alt(_convert_error)
        .alt(raise_exception)
        .unwrap()
    )
    token = token_service.generate_jwt_token(registered_user)
    return UserDetailsApiResponse.from_user(registered_user, token)
