import unittest
import os
from io import BytesIO
from unittest.mock import Mock, patch

from fastapi import UploadFile

from services import upload_services

class UploadServices_Should(unittest.TestCase):
    def test_uploadPictureInCorrectTable(self):
        payload = {'id': 1, 'group': 'admins'}
        image = b'Blob'
        with patch('services.upload_services.update_query') as update_query:
            update_query.return_value = 'admin case'
            result = upload_services.upload_picture(payload, image)

        self.assertEqual('admin case', result)

        payload['group'] = 'companies'
        with patch('services.upload_services.update_query') as update_query:
            update_query.return_value = 'company case'
            result = upload_services.upload_picture(payload, image)

        self.assertEqual('company case', result)

        payload['group'] = 'seekers'
        with patch('services.upload_services.update_query') as update_query:
            update_query.return_value = 'seeker case'
            result = upload_services.upload_picture(payload, image)

        self.assertEqual('seeker case', result)

    def test_getPictureReturnsFromCorrectTable(self):
        user_id = 1
        user_group = 'admins'
        with patch('services.upload_services.read_query') as read_query:
            read_query.return_value = [(b'Blob from admins',)]
            result = upload_services.get_picture(user_id, user_group)

        self.assertEqual(b'Blob from admins', result)

        user_group = 'companies'
        with patch('services.upload_services.read_query') as read_query:
            read_query.return_value = [(b'Blob from companies',)]
            result = upload_services.get_picture(user_id, user_group)

        self.assertEqual(b'Blob from companies', result)

        user_group = 'seekers'
        with patch('services.upload_services.read_query') as read_query:
            read_query.return_value = [(b'Blob from job_seekers',)]
            result = upload_services.get_picture(user_id, user_group)

        self.assertEqual(b'Blob from job_seekers', result)

    def test_isFileJpeg_TrueIfJPG(self):
        cwd = os.path.abspath(os.path.dirname(__file__))
        subpath = 'images/JPG.jpg'
        file_path = os.path.join(cwd, subpath)

        with open(file_path, 'rb') as file:
            file_data = file.read()

        binary_object = BytesIO(file_data)
        upload_file = UploadFile(binary_object)

        result = upload_services.is_file_jpeg(upload_file)

        self.assertEqual(True, result)

    def test_isFileJpeg_FalseIfNotJPG(self):
        cwd = os.path.abspath(os.path.dirname(__file__))
        subpath = 'images/PNG.png'
        file_path = os.path.join(cwd, subpath)

        with open(file_path, 'rb') as file:
            file_data = file.read()

        binary_object = BytesIO(file_data)
        upload_file = UploadFile(binary_object)

        result = upload_services.is_file_jpeg(upload_file)

        self.assertEqual(False, result)

    def test_isFileJpeg_RaisesExceptionIfNotImage(self):
        cwd = os.path.abspath(os.path.dirname(__file__))
        subpath = 'images/TEXT.txt'
        file_path = os.path.join(cwd, subpath)

        with open(file_path, 'rb') as file:
            file_data = file.read()

        binary_object = BytesIO(file_data)
        upload_file = UploadFile(binary_object)

        result = upload_services.is_file_jpeg(upload_file)

        self.assertRaises(Exception)