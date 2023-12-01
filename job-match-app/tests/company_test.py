import unittest
from unittest.mock import Mock, patch

from services import company_services


class CompanyServices_Should(unittest.TestCase):

    def test_readCompaniesReturnsListOfData(self):
        pass

    def test_readCompanyAddressReturnsListOfData(self):
        pass

    def test_getCompanyInformationReturnsCompanyObject_IfCompanyFound(self):
        pass

    def test_getCompanyReturnsNone_IfCompanyNotFound(self):
        pass

    def test_getCompanyByEmailInformationReturnsCompanyObject_IfCompanyFound(self):
        pass

    def test_getCompanyByEmailReturnsNone_IfCompanyNotFound(self):
        pass

    def test_findCompanyIdByUsernameReturnsInteger_IfCompanyFound(self):
        pass

    def test_findCompanyIdByUsernameReturnsNone_IfCompanyNotFound(self):
        pass

    def test_checkCompanyExistReturnsTrue_IfCompanyFound(self):
        pass

    def test_checkCompanyExistReturnsFalse_IfCompanyNotFound(self):
        pass

    def test_createCompanyUsesInsertQueryTwice(self):
        pass

    def test_createCompany_UsesGetPasswordHash(self):
        pass

    def test_createCompany_ReturnsCompany(self):
        pass

    def test_locationIdReturnsInteger_IfCompanyFound(self):
        pass

    def test_locationIdReturnsNone_IfCompanyNotFound(self):
        pass

    def test_getCompanyInfoNameReturnsList_IfCompanyFound(self):
        pass

    def test_getCompanyInfoNameReturnsNone_IfCompanyNotFound(self):
        pass

    def test_everythingFromCompaniesByUsernameReturnsList_IfCompanyFound(self):
        pass

    def test_everythingFromCompaniesByUsernameReturnsNone_IfCompanyNotFound(self):
        pass

    def test_editCompanyInformationReturnsCompany(self):
        pass

    def test_editCompanyInformationUsesUpdateQueryOrUpdateQueriesTransaction(self):
        pass

    def test_editCompanyInformationUsesInsertQuery_IfLocationDoesNotExist(self):
        pass

    def test_findCompanyIdByUsernameForJobSeeker_ReturnsString_IfIdExists(self):
        pass

    def test_findCompanyIdByUsernameForJobSeeker_ReturnsNone_IfIdDoesNotExist(self):
        pass

    def test_viewAllCvsReturnsListOfDicts_IfActiveCvs(self):
        pass

    def test_viewAllCvsReturnsNotFound_IfNoCvs(self):
        pass

    def test_findMatchedJobAds_ReturnsNumberOfArchivedJobAds(self):
        pass
