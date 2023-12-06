from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Job_ad(BaseModel):
    description: str
    location_name: Optional[str]
    remote_status: bool
    min_salary: int
    max_salary: int
    status: str
    date_posted: datetime

    @classmethod
    def from_query_results(cls, description, location_name, remote_status, min_salary, max_salary, status, date_posted):
        return cls(
            description=description,
            location_name=location_name,
            remote_status=remote_status,
            min_salary=min_salary,
            max_salary=max_salary,
            status=status,
            date_posted=date_posted
        )
