from app_models.admin_models import Admin
from data.database import insert_query, insert_transaction_across_tables


def create_admin(new_admin: Admin):
    admin_data = ('''
    INSERT INTO admin_list
    (username, password, role, locked, registration_date)
    VALUES (?,?,?,?,?,?)
    ''')

    insert_transaction_across_tables()