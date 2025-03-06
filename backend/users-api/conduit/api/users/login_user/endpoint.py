from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException, status
from returns.functions import raise_exception

from conduit.api.openapi.unauthorized_error import unauthorized_error_no_body
from conduit.api.openapi.validation_error import validation_error
from conduit.api.security.auth_token_service import AuthTokenService
from conduit.api.tags import Tag
from conduit.api.users.contracts import LoginUserApiRequest, UserDetailsApiResponse
from conduit.application.common.errors import InvalidCredentialsError
from conduit.application.users.use_cases.login_user.use_case import LoginUserUseCase
from conduit.containers import Container

router = APIRouter()


def _convert_error(exc: Exception) -> HTTPException:
    if isinstance(exc, InvalidCredentialsError):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid request",
    )


@router.post(
    path="/users/login",
    responses={
        **unauthorized_error_no_body(),
        **validation_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="Log in a user",
    tags=[Tag.Users],
)
@inject
async def login_user(
    request: Annotated[LoginUserApiRequest, Body()],
    login_user: LoginUserUseCase = Depends(Provide[Container.login_user_use_case]),  # noqa: FAST002
    token_service: AuthTokenService = Depends(Provide[Container.auth_token_service]),  # noqa: FAST002
) -> UserDetailsApiResponse:
    user = (
        (await login_user(request.to_command()))
        .alt(_convert_error)
        .alt(raise_exception)
        .unwrap()
    )
    token = token_service.generate_jwt_token(user)
    return UserDetailsApiResponse.from_user(user, token)
