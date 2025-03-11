from typing import final

from pydantic import HttpUrl


@final
class ImageUrl(HttpUrl):
    pass
