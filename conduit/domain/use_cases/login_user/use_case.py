from conduit.domain.entities.users import LoggedInUser, UserLoginDetails
from conduit.domain.repositories.unit_of_work import UnitOfWork
from conduit.domain.services.users.auth_token_service import AuthTokenService
from conduit.domain.services.users.password_service import PasswordChecker
from conduit.domain.use_cases.login_user.exceptions import InvalidCredentialsException
from conduit.time import CurrentTime


class LoginUserUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        password_checker: PasswordChecker,
        auth_token_service: AuthTokenService,
        now: CurrentTime,
    ):
        self._uow = unit_of_work
        self._password_checker = password_checker
        self._token_service = auth_token_service
        self._now = now

    async def __call__(self, login_details: UserLoginDetails) -> LoggedInUser:
        async with self._uow.begin() as db:
            user = await db.users.get_by_email_or_none(login_details.email)

        if user is None:
            raise InvalidCredentialsException(
                field="email",
                reason=f"There is no user with email '{login_details.email}'",
            )

        if not self._password_checker(login_details.password, user.password_hash):
            raise InvalidCredentialsException(
                field="password",
                reason=f"Incorrect password",
            )

        token = self._token_service.generate_jwt_token(user, self._now())
        return user.to_logged_in_user(token)
