from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status

from conduit.api import open_api
from conduit.api.endpoints.users.contract import (
    RegisterUserApiRequest,
    UserDetailsApiResponse,
)
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.use_cases.register_user.use_case import RegisterUserUseCase

router = APIRouter()


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
    request: Annotated[
        RegisterUserApiRequest,
        Body(),
    ],
    register_user: RegisterUserUseCase = Depends(  # noqa: FAST002
        Provide[Container.register_user_use_case]
    ),
) -> UserDetailsApiResponse:
    registered_user = await register_user(request.to_domain())
    return UserDetailsApiResponse.from_registered_user(registered_user)
