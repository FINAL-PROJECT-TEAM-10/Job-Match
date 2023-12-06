from typing import Annotated

from pydantic import StringConstraints

ALLOWED_USERNAME = Annotated[str, StringConstraints(min_length=3, max_length=20)]
ALLOWED_PASSWORD = Annotated[str, StringConstraints(min_length=5, max_length=30)]
