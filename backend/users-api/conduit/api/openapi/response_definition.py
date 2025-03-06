from typing import Any, Union

from typing_extensions import TypeAlias

OpenApiResponseDefinition: TypeAlias = dict[Union[int, str], dict[str, Any]]
