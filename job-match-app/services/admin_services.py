from app_models.admin_models import Admin
from data.database import insert_query, read_query, update_query


# TODO: Perhaps take the location and other repeatable checks in a separate service
def find_location_id(city: str, country: str):
    location_id = read_query('''SELECT id from locations WHERE city = ? AND country = ?''',
                             (city, country))

    if location_id:
        return location_id[0][0]


def create_location(city: str, country: str):
    new_location_id = insert_query('''
    INSERT INTO locations (city, country)
    VALUES (?,?)
    ''', (city, country))

    return new_location_id


def admin_exists(admin: Admin) -> bool:
    return any(read_query('''SELECT id from admins WHERE username = ?''',
                          (admin.username,)))


def get_admin(username) -> None | Admin:
    admin_data = read_query('''
    SELECT a.id, a.username, a.first_name, a.last_name, a.picture, c.email, c.address, c.telephone, l.city, l.country
    FROM admins as a, employee_contacts as c, locations as l 
    WHERE a.employee_contacts_id = c.id AND c.locations_id = l.id
    AND a.username = ?
    ''', (username,))

    return next((Admin.from_query_results(*row) for row in admin_data), None)


def get_admin_by_email(email):
    admin_data = read_query('''
    SELECT a.id, a.username, a.first_name, a.last_name, a.picture, c.email, c.address, c.telephone, l.city, l.country
    FROM admins as a, employee_contacts as c, locations as l 
    WHERE a.employee_contacts_id = c.id AND c.locations_id = l.id
    AND c.email = ?
    ''', (email,))

    return next((Admin.from_query_results(*row) for row in admin_data), None)


def create_admin(new_admin: Admin, password):
    from services.authorization_services import get_password_hash

    location_id = find_location_id(new_admin.city, new_admin.country)
    if not location_id:
        location_id = create_location(new_admin.city, new_admin.country)

    password = get_password_hash(password)

    contacts_id = insert_query('''
    INSERT INTO employee_contacts
    (email, address, telephone, locations_id)
    VALUES (?,?,?,?)
    ''', (new_admin.email, new_admin.address, new_admin.phone,
          location_id))

    admin_id = insert_query('''
    INSERT INTO admins
    (username, password, first_name, last_name, picture, employee_contacts_id)
    VALUES (?,?,?,?,?,?)
    ''', (new_admin.username, password, new_admin.first_name, new_admin.last_name,
          new_admin.picture, contacts_id))

    new_admin.id = admin_id

    return new_admin


# Use below with caution. All rows with temporary tokens will be dropped.
def delete_temp_tokens():
    update_query('''DELETE FROM temporary_tokens''', (None,))