# COMPANY ADS - CVS
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CvCreation(BaseModel):
    description: str
    location_name: str
    remote_status: bool
    min_salary: int
    max_salary: int
    status: str
    date_posted: datetime

    @classmethod
    def from_query_results(cls, description, city, remote_status, min_salary, max_salary, status, date_posted):
        return cls(
            description=description,
            location_name=city,
            remote_status=remote_status,
            min_salary=min_salary,
            max_salary=max_salary,
            status=status,
            date_posted=date_posted
        )
