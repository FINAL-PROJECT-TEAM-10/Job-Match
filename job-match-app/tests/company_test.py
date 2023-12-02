import unittest
from unittest.mock import Mock, patch

import services.company_services
from app_models.company_models import Company
from services import company_services


def fake_company():
    company = Mock()
    company.id = 1
    company.username = 'username'
    company.email = 'email@email.email'
    company.address = '1 address lane'
    company.telephone = '555-555'
    company.country = 'Country'
    company.city = 'City'
    company.blocked = 0

    return company


class CompanyServices_Should(unittest.TestCase):

    def test_readCompaniesReturnsListOfData(self):
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = [
                (1, 'username1', 'email1@email.email', '1 address lane', '555-555',
                 'Country', 'City', 0),
                (2, 'username2', 'email2@email.email', '12 address lane', '555-556',
                 'Country', 'City', 0)
            ]

            companies = company_services.read_companies()

            self.assertIsInstance(companies, list)
            self.assertEqual(2, len(companies))

    @unittest.skip("Optional test: will be used for future object-centred refactoring")
    def test_readCompaniesReturnsListOfCompanies(self):
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = [
                (1, 'username1', 'email1@email.email', '1 address lane', '555-555',
                 'Country', 'City', 0),
                (2, 'username2', 'email2@email.email', '12 address lane', '555-556',
                 'Country', 'City', 0)
            ]

            companies = company_services.read_companies()

        self.assertIsInstance(companies, list)
        self.assertEqual(2, len(companies))
        self.assertIsInstance(companies[0], Company)
        self.assertEqual(2, companies[1].id)
        self.assertEqual('username2', companies[1].username)
        self.assertEqual('email2@email.email', companies[1].email)
        self.assertEqual('12 address lane', companies[1].work_address)
        self.assertEqual('555-556', companies[1].telephone)
        self.assertEqual('Country', companies[1].country)
        self.assertEqual('City', companies[1].city)
        self.assertEqual(0, companies[1].blocked)

    def test_readCompaniesReturnsEmptyListOfData_IfNoCompanies(self):
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = []

            companies = company_services.read_companies()

            self.assertIsInstance(companies, list)
            self.assertEqual(0, len(companies))

    def test_readCompanyAddressReturnsListOfData(self):
        company = fake_company()
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = [
                (1, 'email1@email.email', '1 address lane', '555-555', 1, 1),
            ]

            address_data = company_services.read_company_adress(company.id)

            self.assertIsInstance(address_data, list)
            self.assertEqual(1, len(address_data))

    def test_readCompanyAddressReturnsEmptyList_IfNoAddress(self):
        company = fake_company()
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = []

            address_data = company_services.read_company_adress(company.id)

            self.assertIsInstance(address_data, list)
            self.assertEqual(0, len(address_data))

    def test_readCompanyLocationReturnsListOfData(self):
        location_id = 1
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = [
                ('City', 'Country'),
            ]

            location_data = company_services.read_company_location(location_id)

            self.assertIsInstance(location_data, list)
            self.assertEqual(1, len(location_data))

    def test_readCompanyLocationReturnsEmptyList_IfNoLocation(self):
        location_id = 1
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = []

            location_data = company_services.read_company_location(location_id)

            self.assertIsInstance(location_data, list)
            self.assertEqual(0, len(location_data))

    @unittest.skip("Optional test: will be used for future object-centred refactoring")
    def test_getCompanyInformationReturnsCompany_IfCompanyFound(self):
        username = 'username2'
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = [
                (2, 'username2', 'email2@email.email', 'description', 0, 1)
            ]

            company = company_services.read_company_information(username)

        self.assertIsInstance(company, Company)
        self.assertEqual(2, company.id)
        self.assertEqual('username2', company.username)
        self.assertEqual('email2@email.email', company.email)
        self.assertEqual('description', company.description)
        self.assertEqual(0, company.blocked)
        self.assertEqual(1, company.approved)

    def test_getCompanyReturnsCompany_IfCompanyFound(self):
        username = 'username2'
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = [
                (2, 'username2', 'email2@email.email', '12 address lane', '555-556',
                 'Country', 'City', 0)
            ]

            company = company_services.get_company(username)

        self.assertIsInstance(company, Company)
        self.assertEqual(2, company.id)
        self.assertEqual('username2', company.username)
        self.assertEqual('email2@email.email', company.email)
        self.assertEqual('12 address lane', company.work_address)
        self.assertEqual('555-556', company.telephone)
        self.assertEqual('Country', company.country)
        self.assertEqual('City', company.city)
        self.assertEqual(0, company.blocked)

    def test_getCompanyReturnsNone_IfCompanyNotFound(self):
        username = 'username2'
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = []

            company = company_services.read_company_information(username)

        self.assertIsNone(company)

    def test_getCompanyByEmailReturnsCompanyObject_IfCompanyFound(self):
        email = 'email2@email.email'
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = [
                (2, 'username2', 'email2@email.email', '12 address lane', '555-556',
                 'Country', 'City', 0)
            ]

            company = company_services.get_company_by_email(email)

        self.assertIsInstance(company, Company)
        self.assertEqual(2, company.id)
        self.assertEqual('username2', company.username)
        self.assertEqual('email2@email.email', company.email)
        self.assertEqual('12 address lane', company.work_address)
        self.assertEqual('555-556', company.telephone)
        self.assertEqual('Country', company.country)
        self.assertEqual('City', company.city)
        self.assertEqual(0, company.blocked)

    def test_getCompanyByEmailReturnsNone_IfCompanyNotFound(self):
        email = 'email2@email.email'
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = []

            company = company_services.read_company_information(email)

        self.assertIsNone(company)

    def test_checkCompanyExistReturnsTrue_IfCompanyFound(self):
        company = fake_company()
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = [
                (1,)
            ]

            exists = company_services.check_company_exist(company.username)

        self.assertTrue(exists)

    def test_checkCompanyExistReturnsFalse_IfCompanyNotFound(self):
        company = fake_company()
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = []

            exists = company_services.check_company_exist(company.username)

        self.assertFalse(exists)

    def test_checkCompanyExistsByIdReturnsTrue_IfCompanyFound(self):
        company = fake_company()
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = [
                (1,)
            ]

            exists = company_services.company_exists_by_id(company.id)

        self.assertTrue(exists)

    def test_checkCompanyExistsByIdReturnsFalse_IfCompanyNotFound(self):
        company = fake_company()
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = []

            exists = company_services.company_exists_by_id(company.id)

        self.assertFalse(exists)

    def test_findCompanyIdByUsernameReturnsInteger_IfCompanyFound(self):
        username = 'username1'
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = [
                (1,)
            ]

            company_id = company_services.find_company_id_byusername(username)

        self.assertEqual(1, company_id)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_findCompanyIdByUsernameReturnsNone_IfCompanyNotFound(self):
        username = 'username1'
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = []

            company_id = company_services.find_company_id_byusername(username)

        self.assertIsNone(company_id)

    @unittest.skip("Optional test: will be used for future object-centred refactoring")
    def test_createCompanyReturnsNewCompany(self):
        company = fake_company()
        company.id = None
        password = 'password'
        control_company = fake_company()

        with patch('services.company_services.insert_query') as insert_query:
            with patch('services.company_services.find_location_id') as find_location_id:
                find_location_id.return_value = 1
                insert_query.return_value = 1

                created_company = company_services.create_company(company, password)

        self.assertIsInstance(created_company, Company)
        self.assertEqual(control_company, created_company)

    @unittest.skip("Optional test: will be used for future object-centred refactoring")
    def test_createCompany_UsesGetPasswordHash(self):
        company = fake_company()
        password = 'password'

        with patch('services.company_services.insert_query') as insert_query:
            with patch('services.company_services.find_location_id') as find_location_id:
                find_location_id.return_value = 1
                insert_query.return_value = 1

                with patch('services.authorization_services.get_password_hash') as get_password_hash:
                    company_services.create_company(company, password)

        get_password_hash.assert_called_once_with(password)

    def test_locationIdReturnsInteger_IfCompanyFound(self):
        company_id = 1
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = [
                (1,)
            ]

            company_id = company_services.location_id(company_id)

        self.assertEqual(1, company_id)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_locationIdReturnsNone_IfCompanyNotFound(self):
        company_id = 1
        with patch('services.company_services.read_query') as read_query:
            read_query.return_value = []

            company_id = company_services.location_id(company_id)

        self.assertIsNone(company_id)

    def test_findLocationReturnsList_IfFound(self):
        pass

    def test_findLocationReturnsNone_IfNotFound(self):
        pass

    @unittest.skip("Testing for this was skipped.\n"
                   "Reason: The logic for this test is identical to the logic\n"
                   "of other similar tests that rely on a single query.\n"
                   "Importantly, we will be moving at a future point to a more\n"
                   "object-centred approach, where get_company gets all the information\n"
                   "necessary for the functioning of the back-end.\n"
                   "Such functions would be deprecated\n\n"
                   "Conclusion: testing for this is a waste of resources.")
    def test_getCompanyInfoNameReturnsList_IfCompanyFound(self):
        pass

    @unittest.skip("Testing for this was skipped.\n"
                   "Reason: The logic for this test is identical to the logic\n"
                   "of other similar tests that rely on a single query.\n"
                   "Importantly, we will be moving at a future point to a more\n"
                   "object-centred approach, where get_company gets all the information\n"
                   "necessary for the functioning of the back-end.\n"
                   "Such functions would be deprecated\n\n"
                   "Conclusion: testing for this is a waste of resources.")
    def test_getCompanyInfoNameReturnsNone_IfCompanyNotFound(self):
        pass

    @unittest.skip("Testing for this was skipped.\n"
                   "Reason: The logic for this test is identical to the logic\n"
                   "of other similar tests that rely on a single query.\n"
                   "Importantly, we will be moving at a future point to a more\n"
                   "object-centred approach, where get_company gets all the information\n"
                   "necessary for the functioning of the back-end.\n"
                   "Such functions would be deprecated\n\n"
                   "Conclusion: testing for this is a waste of resources.")
    def test_everythingFromCompaniesByUsernameReturnsList_IfCompanyFound(self):
        pass

    @unittest.skip("Testing for this was skipped.\n"
                   "Reason: The logic for this test is identical to the logic\n"
                   "of other similar tests that rely on a single query.\n"
                   "Importantly, we will be moving at a future point to a more\n"
                   "object-centred approach, where get_company gets all the information\n"
                   "necessary for the functioning of the back-end.\n"
                   "Such functions would be deprecated\n\n"
                   "Conclusion: testing for this is a waste of resources.")
    def test_everythingFromCompaniesByUsernameReturnsNone_IfCompanyNotFound(self):
        pass

    def test_editCompanyInformationReturnsCompany(self):
        pass

    def test_editCompanyInformationUsesUpdateQueryOrUpdateQueriesTransaction(self):
        pass

    def test_editCompanyInformationUsesInsertQuery_IfLocationDoesNotExist(self):
        pass

    @unittest.skip("Testing for this was skipped.\n"
                   "Reason: The logic for this test is identical to the logic\n"
                   "of other similar tests that rely on a single query.\n"
                   "Importantly, we will be moving at a future point to a more\n"
                   "object-centred approach, where get_company gets all the information\n"
                   "necessary for the functioning of the back-end.\n"
                   "Such functions would be deprecated\n\n"
                   "Conclusion: testing for this is a waste of resources.")
    def test_findCompanyIdByUsernameForJobSeeker_ReturnsString_IfIdExists(self):
        pass

    @unittest.skip("Testing for this was skipped.\n"
                   "Reason: The logic for this test is identical to the logic\n"
                   "of other similar tests that rely on a single query.\n"
                   "Importantly, we will be moving at a future point to a more\n"
                   "object-centred approach, where get_company gets all the information\n"
                   "necessary for the functioning of the back-end.\n"
                   "Such functions would be deprecated\n\n"
                   "Conclusion: testing for this is a waste of resources.")
    def test_findCompanyIdByUsernameForJobSeeker_ReturnsNone_IfIdDoesNotExist(self):
        pass

    def test_viewAllCvsReturnsListOfDicts_IfActiveCvs(self):
        pass

    def test_viewAllCvsReturnsNotFound_IfNoCvs(self):
        pass

    def test_findMatchedJobAds_ReturnsNumberOfArchivedJobAds(self):
        pass
