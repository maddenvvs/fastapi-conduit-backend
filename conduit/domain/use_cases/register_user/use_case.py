from typing import final

from conduit.domain.entities.users import (
    CreateUserDetails,
    RegisteredUser,
    RegisterUserDetails,
    User,
)
from conduit.domain.repositories.users import UsersRepository
from conduit.domain.services.auth_token_service import AuthTokenService
from conduit.domain.services.password_service import PasswordHasher
from conduit.domain.unit_of_work import UnitOfWorkFactory
from conduit.domain.use_cases.register_user.exceptions import (
    EmailAlreadyTakenException,
    UserNameAlreadyTakenException,
)


@final
class RegisterUserUseCase:

    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        users_repository: UsersRepository,
        auth_token_service: AuthTokenService,
        password_hasher: PasswordHasher,
    ) -> None:
        self._uow_factory = uow_factory
        self._users_repository = users_repository
        self._auth_token_service = auth_token_service
        self._password_hasher = password_hasher

    async def __call__(
        self, register_user_details: RegisterUserDetails
    ) -> RegisteredUser:
        return await self._register_user(register_user_details)

    async def _register_user(
        self, register_user_details: RegisterUserDetails
    ) -> RegisteredUser:
        created_user = await self._create_user(register_user_details)
        jwt_token = self._auth_token_service.generate_jwt_token(created_user)
        return created_user.to_registered_user(token=jwt_token)

    async def _create_user(self, register_user_details: RegisterUserDetails) -> User:
        async with self._uow_factory():
            if await self._users_repository.get_by_email_or_none(
                email=register_user_details.email
            ):
                raise EmailAlreadyTakenException(email=register_user_details.email)

            if await self._users_repository.get_by_username_or_none(
                username=register_user_details.username
            ):
                raise UserNameAlreadyTakenException(
                    username=register_user_details.username
                )

            hashed_password = self._password_hasher(register_user_details.password)
            return await self._users_repository.add(
                CreateUserDetails(
                    email=register_user_details.email,
                    username=register_user_details.username,
                    password_hash=hashed_password,
                )
            )
