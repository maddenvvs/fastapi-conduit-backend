from conduit.domain.entities.users import LoggedInUser, UserLoginDetails
from conduit.domain.repositories.users import UsersRepository
from conduit.domain.services.auth_token_service import AuthTokenService
from conduit.domain.services.password_service import PasswordChecker
from conduit.domain.unit_of_work import UnitOfWorkFactory
from conduit.domain.use_cases.login_user.exceptions import InvalidCredentialsError
from conduit.infrastructure.current_time import CurrentTime


class LoginUserUseCase:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        users_repository: UsersRepository,
        password_checker: PasswordChecker,
        auth_token_service: AuthTokenService,
        now: CurrentTime,
    ):
        self._uow_factory = uow_factory
        self._users_repository = users_repository
        self._password_checker = password_checker
        self._token_service = auth_token_service
        self._now = now

    async def __call__(self, login_details: UserLoginDetails) -> LoggedInUser:
        async with self._uow_factory():
            user = await self._users_repository.get_by_email_or_none(
                login_details.email,
            )

        if user is None:
            raise InvalidCredentialsError("There is no user with provided email")

        if not self._password_checker(login_details.password, user.password_hash):
            raise InvalidCredentialsError("Incorrect password")

        token = self._token_service.generate_jwt_token(user, self._now())
        return user.to_logged_in_user(token)
