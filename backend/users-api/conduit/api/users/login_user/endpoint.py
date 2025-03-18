from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status
from returns.functions import raise_exception
from returns.result import Result

from conduit.api.tags import Tag
from conduit.api.users.contracts import LoginUserApiRequest, UserDetailsApiResponse
from conduit.application.users.use_cases.login_user.use_case import LoginUserUseCase
from conduit.containers import Container
from conduit.shared.api.errors.mappers import map_application_error
from conduit.shared.api.openapi.unauthorized_error import unauthorized_error_no_body
from conduit.shared.api.openapi.validation_error import validation_error
from conduit.shared.api.security.auth_token_service import AuthTokenService

router = APIRouter()


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
    user = await login_user(request.to_command())
    token = user.map(lambda user: token_service.generate_jwt_token(str(user.id)))

    return (
        Result.do(UserDetailsApiResponse.from_user(u, t) for u in user for t in token)
        .alt(map_application_error)  # type: ignore
        .alt(raise_exception)
        .unwrap()
    )
