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

    def test_miniCvDescriptionReturnsString(self):
        pass

    def test_miniCvDescriptionReturnsNone_IfNoDescription(self):
        pass

    def test_miniCvMiniSalaryReturnsInt(self):
        # TODO: Check if database returns int by default
        pass

    def test_miniCvMiniSalaryReturnsNone_IfNoMinSalary(self):
        pass

    def test_miniCvMaxSalaryReturnsInt(self):
        # TODO: Check if database returns int by default
        pass

    def test_miniCvMaxSalaryReturnsNone_IfNoMaxSalary(self):
        pass

    def test_miniCvDateCreationReturnsDate(self):
        pass

    def test_miniCvDateCreationReturnsNone_IfNoDate(self):
        pass

    def test_cancelRequest_RaisesOkExceptionWhenSuccessful(self):
        pass

    # TODO: Below might not be in final version
    def test_cancelRequest_RaisesExceptionWhenNotSuccessful(self):
        pass

    def test_checkIfCanceledReturnsTrue_IfCancelled(self):
        pass

    def test_checkIfCanceledReturnsFalse_IfNotCanceled(self):
        pass

    def test_checkRequestExistsReturnsTrue_IfExists(self):
        pass

    def test_checkRequestExistsReturnsFalse_IfNotFalse(self):
        pass

    def test_successfulMatchesReturnsDictInList_IfMatches(self):
        pass

    def test_successfulMatchesReturnsNone_IfNoMatches(self):
        pass
