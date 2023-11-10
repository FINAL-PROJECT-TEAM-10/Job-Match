from app_models.job_seeker_models import JobSeeker
from data.database import read_query


# TODO: Consider having a more encompassing get function
def get_seeker(username) -> None | JobSeeker:
    seeker_data = read_query('''
        SELECT js.id, js.username, ec.email, js.first_name, js.last_name, js.summary, js.blocked
        FROM job_seekers as js, employee_contacts as ec
        WHERE js.employee_contacts_id = ec.id AND js.username = ?
        ''', (username,))

    return next((JobSeeker.from_query_results(*row) for row in seeker_data), None)
