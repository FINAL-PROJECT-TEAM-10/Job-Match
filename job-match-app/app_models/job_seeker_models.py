#PROFESSIONALS - JOB SEEKERS
from pydantic import BaseModel
from typing import Optional

class JobSeeker(BaseModel):
    username: str
    first_name: str
    last_name: str
    summary: str


class JobSeekerInfo(BaseModel):

    summary: Optional[str]
    location : Optional[str]
    status: Optional[str]

class JobSeekerOptionalInfo:
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    summary: Optional[str] = None
    status: Optional[str] = None
    city: Optional[str] = None

    @classmethod
    def from_query_result(cls, username, first_name,last_name, summary,status):
        return cls(username = username,
                   first_name = first_name,
                   last_name = last_name,
                   summary = summary,
                   status = status
            )
