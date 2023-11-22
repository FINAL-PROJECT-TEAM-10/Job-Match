from data.database import update_query, read_query
from PIL import Image

def upload_picture(payload, image_data):
    if payload['group'] == 'admins':
        return update_query('''UPDATE admins SET picture = ? WHERE id = ?''',
                            (image_data, payload['id']))
    if payload['group'] == 'companies':
        return update_query('''UPDATE companies SET picture = ? WHERE id = ?''',
                            (image_data, payload['id']))
    if payload['group'] == 'seekers':
        return update_query('''UPDATE job_seekers SET picture = ? WHERE id = ?''',
                            (image_data, payload['id']))


def get_picture(user_id, user_group):
    if user_group == 'admins':
        return read_query('''SELECT picture FROM admins WHERE id = ?''',
                          (user_id,))[0][0]
    if user_group == 'companies':
        return read_query('''SELECT picture FROM companies WHERE id = ?''',
                          (user_id,))[0][0]
    if user_group == 'seekers':
        return read_query('''SELECT picture FROM job_seekers WHERE id = ?''',
                          (user_id,))[0][0]


def is_file_jpeg(file):
    _ALLOWED_TYPES = {'jpg', 'jpeg'}

    try:
        with Image.open(file.file) as img:
            image_type = img.format.lower()

            if image_type is None:
                return False
            return image_type in _ALLOWED_TYPES
    except Exception as e:
        return f"Image could not be tested: {e}"