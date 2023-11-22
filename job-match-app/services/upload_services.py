from data.database import update_query, read_query
import imghdr


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
        return read_query('''SELECT picture FROM admins WHERE id = ?''', (user_id,))
    if user_group == 'companies':
        return read_query('''SELECT picture FROM companies WHERE id = ?''', (user_id,))
    if user_group == 'seekers':
        return read_query('''SELECT picture FROM job_seekers WHERE id = ?''', (user_id,))


def is_file_jpeg(file):
    _ALLOWED_TYPES = {'jpg', 'jpeg'}

    image_type = imghdr.what(None, h=file.read(32))
    file.seek(0)

    return image_type in _ALLOWED_TYPES
