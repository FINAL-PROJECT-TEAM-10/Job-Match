from typing import Optional

from pydantic import BaseModel

# TODO: Look into BLOBs for picture

# TODO: Consider shortened or full class (full class at the bottom of module)

# Shortened class from Ivaylo's Branch
class JobSeeker(BaseModel):
    id: Optional[int] = None
    group: str = 'seekers'
    username: str
    first_name: str
    email: str
    last_name: str
    summary: str
    blocked: Optional[bool] = 0

    @classmethod
    def from_query_results(cls, id, username, email,
                           first_name, last_name, summary, blocked):
        return cls(id=id, group='seekers', username=username, email=email,
                   first_name=first_name,
                   last_name=last_name,
                   summary=summary,
                   blocked=blocked)

# class Job_Seeker(BaseModel):
#     id: Optional[int] = None
#     username: str
#     first_name: str
#     last_name: str
#     summary: Optional[str] = None
#     picture: Optional[str] = None
#     busy: bool
#     blocked: bool
#     approved: bool
#
#     email = str
#     address = Optional[str] = None
#     phone = Optional[str] = None
#     post_code = Optional[str] = None
#
#     location = str

