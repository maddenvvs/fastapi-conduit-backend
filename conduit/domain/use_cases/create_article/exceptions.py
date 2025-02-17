from typing import final

from conduit.domain.exceptions import DomainException


@final
class ArticleProfileMissingException(DomainException):
    pass
