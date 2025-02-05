from conduit.domain.entities.users import LoggedInUser, UserLoginDetails


class UserAuthService:
    async def login_user(self, login_details: UserLoginDetails) -> LoggedInUser:
        return LoggedInUser(
            email=login_details.email,
            token="jwt.token.here",
            username="jake",
            bio="I work at statefarm",
            image="",
        )
