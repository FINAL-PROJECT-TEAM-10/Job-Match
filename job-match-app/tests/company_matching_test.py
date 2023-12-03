import unittest

from unittest.mock import Mock, patch

import services.company_matching_services
from services import company_matching_services


def fake_job_ad():
    job_ad = Mock()
    job_ad.id = 1
    job_ad.description = 'description'

    return job_ad


def fake_mini_cv():
    cv = Mock()
    cv.id = 1

    return cv


class CompanyMatching_Should(unittest.TestCase):

    def test_checkJobAdExistReturnsTrue_IfJobAdId(self):
        job_ad = fake_job_ad()
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = [
                ('description',)
            ]

            exists = company_matching_services.check_job_ad_exist(job_ad.id)

        self.assertTrue(exists)

    def test_checkJobAdExistReturnsFalse_IfJobAdNotFound(self):
        job_ad = fake_job_ad()
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = []

            exists = company_matching_services.check_job_ad_exist(job_ad.id)

        self.assertFalse(exists)

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
        job_ad = fake_job_ad()
        cv = fake_mini_cv()
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = [
                (1, 1, 'date', 'match_status', 'sender')
            ]

            exists = company_matching_services.matching_exist(job_ad.id, cv.id)

        self.assertTrue(exists)

    def test_matchingExistsReturnsFalse_IfNoMatch(self):
        job_ad = fake_job_ad()
        cv = fake_mini_cv()
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = []

            exists = company_matching_services.matching_exist(job_ad.id, cv.id)

        self.assertFalse(exists)

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
