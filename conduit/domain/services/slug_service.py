import secrets
from typing import Callable

import slugify
from typing_extensions import TypeAlias

Slugify: TypeAlias = Callable[[str], str]


class SlugService:

    def slugify_string(self, string: str) -> str:
        slugged_string = slugify.slugify(string, lowercase=True)
        unique_code = secrets.token_urlsafe(6)
        return f"{slugged_string}-{unique_code}"
