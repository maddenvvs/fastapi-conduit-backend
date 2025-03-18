from typing import final

from conduit.shared.application.errors import ApplicationError


@final
class ArticleNotFoundError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__("Article not found", *args)


@final
class ArticleWithoutAuthorError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__("Article cannot exist without an author", *args)


@final
class ArticleOwningError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__("Can't manipulate an article the user doesn't own", *args)


@final
class ArticleIsAlreadyFavoritedError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__("Article is already favorited", *args)


@final
class ArticleIsAlreadyUnfavoritedError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__("Article is already unfavorited", *args)


@final
class ProfileNotFoundError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__("Profile not found", *args)


@final
class CannotFollowYourselfError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__("Cannot follow yourself", *args)


@final
class CannotUnfollowYourselfError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__("Cannot unfollow yourself", *args)


@final
class ProfileIsAlreadyFollowedError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__("Profile is already followed", *args)


@final
class ProfileIsAlreadyUnfollowedError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__("Profile is already unfollowed", *args)


@final
class CommentOwnershipError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__("User doesn't own the comment", *args)


class Errors:
    @staticmethod
    def article_not_found() -> ArticleNotFoundError:
        raise ArticleNotFoundError

    @staticmethod
    def article_without_author() -> ArticleWithoutAuthorError:
        return ArticleWithoutAuthorError()

    @staticmethod
    def article_owning_error() -> ArticleOwningError:
        return ArticleOwningError()

    @staticmethod
    def article_is_already_favorited() -> ArticleIsAlreadyFavoritedError:
        return ArticleIsAlreadyFavoritedError()

    @staticmethod
    def article_is_already_unfavorited() -> ArticleIsAlreadyUnfavoritedError:
        return ArticleIsAlreadyUnfavoritedError()

    @staticmethod
    def profile_not_found() -> ProfileNotFoundError:
        return ProfileNotFoundError()

    @staticmethod
    def cannot_follow_yourself() -> CannotFollowYourselfError:
        return CannotFollowYourselfError()

    @staticmethod
    def cannot_unfollow_yourself() -> CannotUnfollowYourselfError:
        return CannotUnfollowYourselfError()

    @staticmethod
    def profile_is_already_followed() -> ProfileIsAlreadyFollowedError:
        return ProfileIsAlreadyFollowedError()

    @staticmethod
    def profile_is_already_unfollowed() -> ProfileIsAlreadyUnfollowedError:
        return ProfileIsAlreadyUnfollowedError()

    @staticmethod
    def comment_ownership() -> CommentOwnershipError:
        return CommentOwnershipError()
