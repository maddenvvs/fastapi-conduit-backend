from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from returns.maybe import Maybe, Nothing
from typing_extensions import Never, TypeAlias

from conduit.api.security.auth_token_service import AuthTokenService
from conduit.api.security.errors import Error
from conduit.api.security.http_token_header import HttpTokenHeader
from conduit.application.common.unit_of_work import UnitOfWorkFactory
from conduit.application.users.repositories.users_repository import UsersRepository
from conduit.containers import Container
from conduit.domain.users.user import User

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
async def maybe_get_current_user(
    jwt_token: OptionalJwtToken,
    auth_token_service: AuthTokenService = Depends(
        Provide[Container.auth_token_service],
    ),
    uow_factory: UnitOfWorkFactory = Depends(Provide[Container.uow_factory]),
    users_repository: UsersRepository = Depends(Provide[Container.users_repository]),
) -> Maybe[User]:
    if not jwt_token:
        return Nothing

    token_payload = auth_token_service.parse_jwt_token(jwt_token)

    async with uow_factory():
        return await users_repository.get_by_id(token_payload.user_id)


def _find_user_failure() -> Never:
    raise Error.invalid_token_schema()


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
        user = await users_repository.get_by_id(token_payload.user_id)

    return user.or_else_call(_find_user_failure)


CurrentUser: TypeAlias = Annotated[User, Depends(get_current_user)]
OptionalCurrentUser: TypeAlias = Annotated[
    Maybe[User],
    Depends(maybe_get_current_user),
]
