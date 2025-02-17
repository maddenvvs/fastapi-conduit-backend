from typing import Annotated, Optional

import starlette.status as http_status
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from starlette.exceptions import HTTPException
from typing_extensions import TypeAlias

from conduit.api.security.http_token_header import HttpTokenHeader
from conduit.containers import Container
from conduit.domain.entities.users import User
from conduit.domain.repositories.unit_of_work import UnitOfWork
from conduit.domain.services.auth_token_service import AuthTokenService

token_security = HttpTokenHeader(
    name="Authorization",
    scheme_name="JWT Token",
    description="Token Format: `Token xxxxxx.yyyyyyy.zzzzzz`",
    raise_error=True,
)
optional_token_security = HttpTokenHeader(
    name="Authorization",
    scheme_name="JWT Token",
    description="Token Format: `Token xxxxxx.yyyyyyy.zzzzzz`",
    raise_error=False,
)

JwtToken = Annotated[str, Depends(token_security)]
OptionalJwtToken = Annotated[str, Depends(optional_token_security)]


@inject
async def get_current_user_or_none(
    jwt_token: JwtToken,
    auth_token_service: AuthTokenService = Depends(
        Provide[Container.auth_token_service]
    ),
    unit_of_work: UnitOfWork = Depends(Provide[Container.unit_of_work]),
) -> Optional[User]:
    token_payload = auth_token_service.parse_jwt_token(jwt_token)
    async with unit_of_work.begin() as db:
        return await db.users.get_by_id_or_none(token_payload.user_id)


@inject
async def get_current_user(
    jwt_token: JwtToken,
    auth_token_service: AuthTokenService = Depends(
        Provide[Container.auth_token_service]
    ),
    unit_of_work: UnitOfWork = Depends(Provide[Container.unit_of_work]),
) -> User:
    token_payload = auth_token_service.parse_jwt_token(jwt_token)
    async with unit_of_work.begin() as db:
        user = await db.users.get_by_id_or_none(token_payload.user_id)
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
