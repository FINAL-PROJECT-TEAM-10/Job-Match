from app_models.company_models import Company
from data.database import read_query


# TODO: The get below doesn't consider multiple addresses for a company!!!
#  Consider having a main column to get a company's main address
def get_company(username) -> None | Company:
    company_data = read_query('''
        SELECT c.id, c.username, cc.email, cc.address, cc.telephone, l.country, l.city, c.blocked
        FROM companies as c, company_contacts as cc, locations as l
        WHERE c.username = ? AND cc.company_id = c.id AND cc.locations_id = l.id
        ''', (username,))

    return next((Company.from_query_result(*row) for row in company_data), None)
