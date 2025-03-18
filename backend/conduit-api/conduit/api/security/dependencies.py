from typing import Annotated, Optional

import starlette.status as http_status
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from starlette.exceptions import HTTPException
from typing_extensions import TypeAlias

from conduit.application.common.repositories.users import UsersRepository
from conduit.containers import Container
from conduit.domain.entities.users import User
from conduit.shared.api.security.auth_token_service import AuthTokenService
from conduit.shared.api.security.http_token_header import (
    HttpTokenHeader,
    NoTokenStrategy,
)
from conduit.shared.application.unit_of_work import UnitOfWorkFactory

token_security = HttpTokenHeader(
    name="Authorization",
    scheme_name="JWT Token",
    description="Token Format: `Token xxxxxx.yyyyyyy.zzzzzz`",
    error_strategy=NoTokenStrategy.Raise,
)
optional_token_security = HttpTokenHeader(
    name="Authorization",
    scheme_name="JWT Token",
    description="Token Format: `Token xxxxxx.yyyyyyy.zzzzzz`",
    error_strategy=NoTokenStrategy.Silent,
)

JwtToken = Annotated[str, Depends(token_security)]
OptionalJwtToken = Annotated[str, Depends(optional_token_security)]


@inject
async def get_current_user_or_none(
    jwt_token: OptionalJwtToken,
    auth_token_service: AuthTokenService = Depends(
        Provide[Container.auth_token_service],
    ),
    uow_factory: UnitOfWorkFactory = Depends(Provide[Container.uow_factory]),
    users_repository: UsersRepository = Depends(Provide[Container.users_repository]),
) -> Optional[User]:
    if jwt_token:
        token_payload = auth_token_service.parse_jwt_token(jwt_token)
        async with uow_factory():
            return await users_repository.get_by_user_id_or_none(token_payload.user_id)
    return None


@inject
async def get_current_user(
    jwt_token: JwtToken,
    auth_token_service: AuthTokenService = Depends(
        Provide[Container.auth_token_service],
    ),
    uow_factory: UnitOfWorkFactory = Depends(Provide[Container.uow_factory]),
    users_repository: UsersRepository = Depends(Provide[Container.users_repository]),
) -> User:
    token_payload = auth_token_service.parse_jwt_token(jwt_token)
    async with uow_factory():
        user = await users_repository.get_by_user_id_or_none(token_payload.user_id)
    if user is None:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token schema.",
        )
    return user


CurrentUser: TypeAlias = Annotated[User, Depends(get_current_user)]
OptionalCurrentUser: TypeAlias = Annotated[
    Optional[User],
    Depends(get_current_user_or_none),
]
