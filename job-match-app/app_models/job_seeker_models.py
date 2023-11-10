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
    location : str
    status: str