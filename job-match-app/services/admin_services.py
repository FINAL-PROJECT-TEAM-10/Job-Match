from app_models.admin_models import Admin
from data.database import insert_query


def create_admin(new_admin: Admin):
    insert_query