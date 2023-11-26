import time
import unittest
from unittest.mock import Mock, patch, MagicMock

from fastapi import HTTPException
from fastapi.testclient import TestClient

from common.auth import get_current_user
from main import app
from routers import admin_routers

mock_admin_services = Mock(spec='services.admin_services')
mock_admin_services.create_admin = Mock(return_value='Mocked return')

admin_routers.admin_services = mock_admin_services


def fake_admin_payload():
    payload = MagicMock(spec=dict)
    payload['group'] = 'admins'
    return payload


def fake_regular_payload():
    payload = MagicMock(dict)
    return payload


def fake_admin():
    admin = Mock()
    return admin


class AdminRouter_Should(unittest.TestCase):
    def setUp(self):
        self.original_get_current_user = get_current_user
        mock_admin_services.reset_mock()

    def tearDown(self) -> None:
        get_current_user = self.original_get_current_user

    def test_addAdmin_returnsAdmin(self):
        pass

    def test_addAdmin_raisesExceptionWhenUserNotAdmin(self):
        get_current_user = lambda: {"id": 1,
                                    "group": "companies",
                                    "username": "CompanyUser",
                                    "email": "company@company.com",
                                    "blocked": 0,
                                    'exp': time.time()
                                    }

        # get_current_user = fake_regular_payload()
        new_admin = fake_admin()

        with TestClient(app) as test_client:
            response = test_client.post('/register')

        with self.assertRaises(HTTPException) as e:
            admin_routers.add_admin(new_admin, 'asdQWE123!@#')

        self.assertEqual(e.exception.status_code, 403)

    def test_addAdmin_raisesExceptionWhenAdminExists(self):
        pass

    def test_addAdmin_raisesExceptionWhenAdminCreatesNonAdmin(self):
        pass

    def test_deleteAllTempTokens_raisesExceptionWhenUserNotAdmin(self):
        pass

    def test_getAdminAvatar_returnsStreamingResponse(self):
        pass

    def test_getAdminAvatar_raisesExceptionWhenNoAdmin(self):
        pass

    def test_getAdminAvatar_raisesExceptionWhenNoImage(self):
        pass


class AdminServices_Should(unittest.TestCase):
    def test_adminExists_returnsTrue_ifAdminFound(self):
        pass

    def test_adminExists_returnsFalse_ifNoAdmin(self):
        pass

    def test_adminExistsById_returnsTrue_ifAdminFound(self):
        pass

    def test_adminExistsById_returnsFalse_ifNoAdmin(self):
        pass

    def test_getAdmin_returnsAdmin(self):
        pass

    def test_getAdmin_returnsNoneIfNoAdmin(self):
        pass

    def test_getAdminByEmail_returnsAdmin(self):
        pass

    def test_getAdminByEmail_returnsNoneIfNoAdmin(self):
        pass

    def test_createAdmin_ReturnsAdmin(self):
        pass
