import unittest

from unittest.mock import Mock, patch

from services import company_matching_services

class CompanyMatching_Should(unittest.TestCase):

    def test_checkJobAdExistReturnsTrue_IfJobAdId(self):
        pass

    def test_checkJobAdExistReturnsFalse_IfJobAdNotFound(self):
        pass

    def test_matchCvUsesUpdateQuery_WhenMatchFinalized(self):
        pass

    def test_matchCvUsesInsertQuery_WhenMatchCreated(self):
        pass

    def test_matchCVRaisesCorrectHTTPException_IfMatchHasBeenDone(self):
        pass

    def test_isMainCvReturnsTrue_IfMainCv(self):
        pass

    def test_isMainCvReturnsFalse_IfNotMainCv(self):
        pass

    def test_matchingExistsReturnsTrue_IfMatch(self):
        pass

    def test_matchingExistsReturnsFalse_IfNoMatch(self):
        pass


    def test_pendingCvsReturnsDictInList_IfMiniCv(self):
        pass

    # TODO: Finish structure of unit test after optimizing database interactions


