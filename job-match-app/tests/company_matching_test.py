import unittest
from datetime import datetime

from unittest.mock import Mock, patch

import services.company_matching_services
from services import company_matching_services

from fastapi.exceptions import HTTPException


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
        job_ad = fake_job_ad()
        cv = fake_mini_cv()

        with patch('services.company_matching_services.matching_exist') as matching_exist:
            matching_exist.return_value = True
            with patch('services.company_matching_services.update_query') as update_query:
                update_query.return_value = None

                try:
                    company_matching_services.match_cv(job_ad.id, cv.id)
                except HTTPException:
                    self.assertEqual(2, update_query.call_count)

    def test_matchCvUsesInsertQuery_WhenMatchCreated(self):
        job_ad = fake_job_ad()
        cv = fake_mini_cv()

        with patch('services.company_matching_services.matching_exist') as matching_exist:
            matching_exist.return_value = False
            with patch('services.company_matching_services.insert_query') as insert_query:
                insert_query.return_value = None

                try:
                    company_matching_services.match_cv(job_ad.id, cv.id)
                except HTTPException:
                    insert_query.assert_called_once()



    def test_matchCVRaisesCorrectHTTPException_IfMatchHasBeenDone(self):
        job_ad = fake_job_ad()
        cv = fake_mini_cv()

        with patch('services.company_matching_services.matching_exist') as matching_exist:
            matching_exist.return_value = True
            with patch('services.company_matching_services.update_query') as update_query:
                update_query.return_value = None

                with self.assertRaises(HTTPException) as conflict:
                    company_matching_services.match_cv(job_ad.id, cv.id)
                self.assertEqual(200, conflict.exception.status_code)

            matching_exist.return_value = False
            with patch('services.company_matching_services.insert_query') as insert_query:
                insert_query.return_value = None

                with self.assertRaises(HTTPException) as conflict:
                    company_matching_services.match_cv(job_ad.id, cv.id)
                self.assertEqual(200, conflict.exception.status_code)

    def test_isMainCvReturnsTrue_IfMainCv(self):
        seeker_id = 1
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = [
                (1,)
            ]

            result = company_matching_services.get_main_cv(seeker_id)

        self.assertTrue(result)

    def test_isMainCvReturnsFalse_IfNotMainCv(self):
        seeker_id = 1
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = []

            result = company_matching_services.get_main_cv(seeker_id)

        self.assertFalse(result)

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

    # Below needs to be refactored to Return a List of CVs once we
    # move to objects fully at a future point. Since this is an important method
    # for the current state of the app, it was still tested.
    # SELECTING CV creator and location info with one QUERY should be the goal.
    # Currently, copy-pasted from test_successfulMatchesReturnsDictInList_IfMatches
    # Could be done with a setup/teardown because of similar test.
    def test_pendingCvsReturnsDictInList_IfMiniCv(self):
        job_ad = fake_job_ad()
        with patch('services.company_matching_services.read_query') as read_query, \
                patch('services.company_matching_services.mini_cv_description') as get_description, \
                patch('services.company_matching_services.mini_cv_mini_salary') as get_min_salary, \
                patch('services.company_matching_services.mini_cv_max_salary') as get_max_salary, \
                patch('services.company_matching_services.mini_cv_date_creation') as get_date_created, \
                patch('services.job_seeker_services.get_cv_location_name') as get_location_name, \
                patch('services.job_seeker_services.get_cv_location_id') as get_location_id:
            get_description.return_value = 'description'
            get_min_salary.return_value = 100
            get_max_salary.return_value = 200
            get_date_created.return_value = 'created_date'
            get_location_name.return_value = 'placeholder_loc_name'
            get_location_id.return_value = 'placeholder_loc_id'

            read_query.return_value = [
                (1, 2, 'matched_date', 'match_status', 'sender')
            ]

            cvs = company_matching_services.pending_cvs(job_ad.id)

        self.assertIsInstance(cvs, list)
        self.assertIsInstance(cvs[0], dict)
        self.assertEqual(2, cvs[0]['Mini CV ID'])
        self.assertEqual('description', cvs[0]['Mini CV Description'])
        self.assertEqual(100, cvs[0]['Minimal Salary'])
        self.assertEqual(200, cvs[0]['Maximum Salary'])
        self.assertEqual('placeholder_loc_name', cvs[0]['Preferred Location'])
        self.assertEqual('match_status', cvs[0]['Status'])
        self.assertEqual('created_date', cvs[0]['CV created on'])
        self.assertEqual('matched_date', cvs[0]['Date of match request'])

    def test_successfulMatchesRaisesNotFound_IfNoMatches(self):
        job_ad = fake_job_ad()
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = []

            with self.assertRaises(HTTPException) as conflict:
                cvs = company_matching_services.pending_cvs(job_ad.id)

        self.assertEqual(404, conflict.exception.status_code)

    def test_miniCvDescriptionReturnsString(self):
        cv = fake_mini_cv()
        cv.description = 'description'
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = [
                ('description',)
            ]

            result = company_matching_services.mini_cv_description(cv.id)

        self.assertIsInstance(result, str)
        self.assertEqual(cv.description, result)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_miniCvDescriptionReturnsNone_IfNoDescription(self):
        cv = fake_mini_cv()
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = []

            result = company_matching_services.mini_cv_description(cv.id)

        self.assertIsNone(result)

    def test_miniCvMiniSalaryReturnsInt(self):
        cv = fake_mini_cv()
        cv.min_salary = 100
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = [
                (100,)
            ]

            result = company_matching_services.mini_cv_description(cv.id)

        self.assertIsInstance(result, int)
        self.assertEqual(cv.min_salary, result)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_miniCvMiniSalaryReturnsNone_IfNoMinSalary(self):
        cv = fake_mini_cv()
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = []

            result = company_matching_services.mini_cv_mini_salary(cv.id)

        self.assertIsNone(result)

    def test_miniCvMaxSalaryReturnsInt(self):
        cv = fake_mini_cv()
        cv.max_salary = 200
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = [
                (200,)
            ]

            result = company_matching_services.mini_cv_description(cv.id)

        self.assertIsInstance(result, int)
        self.assertEqual(cv.max_salary, result)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_miniCvMaxSalaryReturnsNone_IfNoMaxSalary(self):
        cv = fake_mini_cv()
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = []

            result = company_matching_services.mini_cv_max_salary(cv.id)

        self.assertIsNone(result)

    def test_miniCvDateCreationReturnsDate(self):
        cv = fake_mini_cv()
        now = datetime.now()
        cv.date = now
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = [
                (now,)
            ]

            result = company_matching_services.mini_cv_description(cv.id)

        self.assertIsInstance(result, datetime)
        self.assertEqual(cv.date, result)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_miniCvDateCreationReturnsNone_IfNoDate(self):
        cv = fake_mini_cv()
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = []

            result = company_matching_services.mini_cv_description(cv.id)

        self.assertIsNone(result)

    def test_cancelRequest_RaisesOkExceptionWhenSuccessful(self):
        pass

    # TODO: Below might not be in final version
    def test_cancelRequest_RaisesExceptionWhenNotSuccessful(self):
        pass

    def test_checkIfCanceledReturnsTrue_IfCancelled(self):
        job_ad = fake_job_ad()
        cv = fake_mini_cv()
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = [
                (1, 1, 'date', 'match_status', 'sender')
            ]

            exists = company_matching_services.check_request_exist(job_ad.id, cv.id)

        self.assertTrue(exists)

    def test_checkIfCanceledReturnsFalse_IfNotCanceled(self):
        job_ad = fake_job_ad()
        cv = fake_mini_cv()
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = []

            exists = company_matching_services.matching_exist(job_ad.id, cv.id)

        self.assertFalse(exists)

    def test_checkRequestExistsReturnsTrue_IfExists(self):
        job_ad = fake_job_ad()
        cv = fake_mini_cv()
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = [
                (1, 1, 'date', 'match_status', 'sender')
            ]

            exists = company_matching_services.check_request_exist(job_ad.id, cv.id)

        self.assertTrue(exists)

    def test_checkRequestExistsReturnsFalse_IfNotFalse(self):
        job_ad = fake_job_ad()
        cv = fake_mini_cv()
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = []

            exists = company_matching_services.matching_exist(job_ad.id, cv.id)

        self.assertFalse(exists)

    # Below needs to be refactored to Return a List of CVs once we
    # move to objects fully at a future point. Since this is an important method
    # for the current state of the app, it was still tested.
    # SELECTING CV creator and location info with one QUERY should be the goal.
    def test_successfulMatchesReturnsDictInList_IfMatches(self):
        with patch('services.company_matching_services.read_query') as read_query, \
                patch('services.company_matching_services.mini_cv_description') as get_description, \
                patch('services.company_matching_services.mini_cv_mini_salary') as get_min_salary, \
                patch('services.company_matching_services.mini_cv_max_salary') as get_max_salary, \
                patch('services.company_matching_services.mini_cv_date_creation') as get_date_created, \
                patch('services.job_seeker_services.get_cv_location_name') as get_location_name, \
                patch('services.job_seeker_services.get_cv_location_id') as get_location_id:
            get_description.return_value = 'description'
            get_min_salary.return_value = 100
            get_max_salary.return_value = 200
            get_date_created.return_value = 'created_date'
            get_location_name.return_value = 'placeholder_loc_name'
            get_location_id.return_value = 'placeholder_loc_id'

            read_query.return_value = [
                (1, 2, 'matched_date', 'match_status', 'sender')
            ]

            cvs = company_matching_services.successfull_matches()

        self.assertIsInstance(cvs, list)
        self.assertIsInstance(cvs[0], dict)
        self.assertEqual(2, cvs[0]['Mini CV ID'])
        self.assertEqual('description', cvs[0]['Mini CV Description'])
        self.assertEqual(100, cvs[0]['Minimal Salary'])
        self.assertEqual(200, cvs[0]['Maximum Salary'])
        self.assertEqual('placeholder_loc_name', cvs[0]['Preferred Location'])
        self.assertEqual('match_status', cvs[0]['Status'])
        self.assertEqual('created_date', cvs[0]['CV created on'])
        self.assertEqual('matched_date', cvs[0]['Date of match request'])

    def test_successfulMatchesReturnsNone_IfNoMatches(self):
        with patch('services.company_matching_services.read_query') as read_query:
            read_query.return_value = []

            cvs = company_matching_services.successfull_matches()

        self.assertIsNone(cvs)
