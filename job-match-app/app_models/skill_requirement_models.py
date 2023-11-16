from typing import Annotated, Optional

from pydantic import BaseModel, StringConstraints


class SkillRequirement(BaseModel):
    id: Optional[int] = None
    name: Annotated[str, StringConstraints(min_length=2, max_length=45)]
    description: Optional[Annotated[str, StringConstraints(min_length=2, max_length=200)]]
    career_type: Optional[Annotated[str, StringConstraints(min_length=2, max_length=45)]]

    @classmethod
    def from_query_results(cls, id, name, description, career_type):
        return cls(id=id, name=name, description=description, career_type=career_type)