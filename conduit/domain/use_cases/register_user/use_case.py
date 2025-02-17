from typing import final

from conduit.domain.entities.users import (
    CreateUserDetails,
    RegisteredUser,
    RegisterUserDetails,
    User,
)
from conduit.domain.repositories.unit_of_work import UnitOfWork
from conduit.domain.services.auth_token_service import AuthTokenService
from conduit.domain.services.password_service import PasswordHasher
from conduit.domain.use_cases.register_user.exceptions import (
    EmailAlreadyTakenException,
    UserNameAlreadyTakenException,
)


@final
class RegisterUserUseCase:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        auth_token_service: AuthTokenService,
        password_hasher: PasswordHasher,
    ) -> None:
        self._uof = unit_of_work
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
        async with self._uof.begin() as db:
            if await db.users.get_by_email_or_none(email=register_user_details.email):
                raise EmailAlreadyTakenException(email=register_user_details.email)

            if await db.users.get_by_username_or_none(
                username=register_user_details.username
            ):
                raise UserNameAlreadyTakenException(
                    username=register_user_details.username
                )

            hashed_password = self._password_hasher(register_user_details.password)
            return await db.users.add(
                CreateUserDetails(
                    email=register_user_details.email,
                    username=register_user_details.username,
                    password_hash=hashed_password,
                )
            )
