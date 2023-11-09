from app_models.admin_models import Admin
from data.database import insert_query, read_query
from services.authorization_services import get_password_hash

# TODO: Perhaps take the location and other repeatable checks in a separate service
def find_location_id(city: str, country: str):
    location_id = read_query('''SELECT id from locations WHERE city = ? AND country = ?''',
                  (city, country))[0][0]

    if location_id:
        return location_id

def create_location(city: str, country: str):
    new_location_id = insert_query('''
    INSERT INTO locations (city, country)
    VALUES (?,?)
    ''', (city, country))

    return new_location_id

def admin_exists(admin) -> bool:
    return any(read_query('''SELECT id from admin_list WHERE username = ?''',
                          (admin.username,)))

def create_admin(new_admin: Admin, password):
    location_id = find_location_id(new_admin.city, new_admin.country)
    if not location_id:
        location_id = create_location(new_admin.city, new_admin.country)

    password = get_password_hash(password)

    contacts_id = insert_query('''
    INSERT INTO employee_contacts
    (email, address, telephone, post_code, locations_id)
    VALUES (?,?,?,?,?)
    ''', (new_admin.email, new_admin.address, new_admin.phone, new_admin.post_code,
                    location_id))

    admin_id = insert_query('''
    INSERT INTO admin_list
    (username, password, first_name, last_name, picture, employee_contacts_id)
    VALUES (?,?,?,?,?,?)
    ''', (new_admin.username, password, new_admin.first_name, new_admin.last_name,
                            new_admin.picture, contacts_id))

    new_admin.id = admin_id

    return new_admin

# _first_admin = Admin(username='first_admin',
#                      first_name='Admin',
#                      last_name='Adminov',
#                      email='admin@admin.admin',
#                      phone='1234567890',
#                      post_code='1000',
#                      city='Sofia',
#                      country='Bulgaria')
# _first_admin_pass = 'asdQWE123!@#'
#
# create_admin(_first_admin, _first_admin_pass)