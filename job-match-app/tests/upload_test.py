import unittest
import os
from io import BytesIO
from unittest.mock import Mock, patch

from fastapi import UploadFile

from services import upload_services

class UploadServices_Should(unittest.TestCase):
    def test_uploadPictureInCorrectTable(self):
        pass

    def test_getPictureReturnsFromCorrectTable(self):
        pass

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