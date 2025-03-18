from fastapi import HTTPException, status

from conduit.shared.application.errors import ApplicationError, InvalidCredentialsError


def map_application_error(exc: ApplicationError) -> HTTPException:
    if isinstance(exc, InvalidCredentialsError):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=exc.message,
    )
