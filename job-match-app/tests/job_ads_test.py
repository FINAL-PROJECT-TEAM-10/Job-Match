import unittest
from datetime import datetime

from unittest.mock import Mock, patch

import mariadb
from fastapi.exceptions import HTTPException

import common.percent_jobad_calculator
import services.job_ads_services
from services import job_ads_services
from app_models.job_ads_models import Job_ad


def fake_job_ad():
    job_ad = Mock()
    job_ad.description = 'description'
    job_ad.location_name = 'city'
    job_ad.remote_status = 0
    job_ad.min_salary = 1000
    job_ad.max_salary = 2000
    job_ad.status = 'status'

    return job_ad


class JobAdsServices_Should(unittest.TestCase):
    # The bottom two tests will be the basis for the object-centred future
    # direction of the project.
    def test_getJobAdAsObject_ReturnsJobAdObject(self):
        job_ad_id = 1
        now = datetime.now()

        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [
                ('description', 'city', 0, 1000, 2000, 'status', now)
            ]

            result = job_ads_services.get_job_ad_as_object(job_ad_id)

        self.assertIsInstance(result, Job_ad)
        self.assertEqual('description', result.description)
        self.assertEqual('city', result.location_name)
        self.assertEqual(0, result.remote_status)
        self.assertEqual(1000, result.min_salary)
        self.assertEqual(2000, result.max_salary)
        self.assertEqual('status', result.status)
        self.assertEqual(now, result.date_posted)

    def test_getJobAdAsObject_ReturnsNone_IfNotFound(self):
        job_ad_id = 1

        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.get_job_ad_as_object(job_ad_id)

        self.assertIsNone(result)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_findCompany_ReturnsInteger(self):
        username = 'company'
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [
                (100,)
            ]

            result = job_ads_services.find_company(username)

        self.assertIsInstance(result, int)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_findCompany_ReturnsNone_IfNotFound(self):
        username = 'company'
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.find_company(username)

        self.assertIsNone(result)

    def test_findNameById_ReturnsStr(self):
        company_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [
                ('username',)
            ]

            result = job_ads_services.find_name_by_id(company_id)

        self.assertIsInstance(result, str)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_findNameById_ReturnsNone_IfNotFound(self):
        company_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.find_name_by_id(company_id)

        self.assertIsNone(result)

    def test_createJobAd_ReturnsJobAd(self):
        job_ad = fake_job_ad()
        company_id = 1
        requirements = []
        requirements_levels = []

        with patch('services.job_ads_services.read_query') as read_query, \
                patch('services.job_ads_services.insert_query') as insert_query, \
                patch('services.job_ads_services.update_query') as update_query, \
                patch('services.company_services.find_location') as fl, \
                patch('services.job_seeker_services.check_skill_exist') as cse:
            read_query.return_value = [(1,)]
            insert_query.return_value = 1
            update_query.return_value = None
            fl.return_value = [(job_ad.location_name,)]
            cse.return_value = True

            result = job_ads_services.create_job_add(
                job_ad.description,
                job_ad.location_name,
                'No',
                job_ad.min_salary,
                job_ad.max_salary,
                job_ad.status,
                company_id,
                requirements,
                requirements_levels
            )

            self.assertIsInstance(result, Job_ad)
            self.assertEqual('description', result.description)
            self.assertEqual('city', result.location_name)
            self.assertEqual(0, result.remote_status)
            self.assertEqual(1000, result.min_salary)
            self.assertEqual(2000, result.max_salary)
            self.assertEqual('status', result.status)

    @unittest.skip("Proud of test: will be used for future bug-testing")
    def test_createJobAd_RaisesException_WhenIntegrityError(self):
        job_ad = fake_job_ad()
        company_id = 1
        requirements = []
        requirements_levels = []

        with patch('services.job_ads_services.read_query') as read_query, \
                patch('services.job_ads_services.insert_query') as insert_query, \
                patch('services.job_ads_services.update_query') as update_query, \
                patch('services.company_services.find_location') as fl, \
                patch('services.job_seeker_services.check_skill_exist') as cse:
            read_query.return_value = [(1,)]
            update_query.return_value = None
            fl.return_value = [(job_ad.location_name,)]
            cse.return_value = True

            insert_query.return_value = 1
            insert_query.side_effect = mariadb.IntegrityError("MockedError")

            with self.assertRaises(HTTPException) as conflict:
                with self.assertRaises(mariadb.IntegrityError):
                    job_ads_services.create_job_add(
                        job_ad.description,
                        job_ad.location_name,
                        job_ad.remote_status,
                        job_ad.min_salary,
                        job_ad.max_salary,
                        job_ad.status,
                        company_id,
                        requirements,
                        requirements_levels
                    )

            self.assertEqual(409, conflict.exception.status_code)

    def test_createJobAd_UsesInsertQuery(self):
        job_ad = fake_job_ad()
        company_id = 1
        requirements = []
        requirements_levels = []

        with patch('services.job_ads_services.read_query') as read_query, \
                patch('services.job_ads_services.insert_query') as insert_query, \
                patch('services.job_ads_services.update_query') as update_query, \
                patch('services.company_services.find_location') as fl:
            read_query.return_value = [(1,)]
            insert_query.return_value = 1
            update_query.return_value = None
            fl.return_value = [(job_ad.location_name,)]

            job_ads_services.create_job_add(
                job_ad.description,
                job_ad.location_name,
                job_ad.remote_status,
                job_ad.min_salary,
                job_ad.max_salary,
                job_ad.status,
                company_id,
                requirements,
                requirements_levels
            )

            insert_query.assert_called()

    def test_createJobAd_RaisesException_IfNoLocationAndNotRemote(self):
        job_ad = fake_job_ad()
        company_id = 1
        requirements = []
        requirements_levels = []

        # Added patch to protect database
        with patch('services.job_ads_services.read_query') as read_query, \
                patch('services.job_ads_services.insert_query') as insert_query, \
                patch('services.job_ads_services.update_query') as update_query:
            read_query.return_value = None
            insert_query.return_value = None
            update_query.return_value = None

            with self.assertRaises(HTTPException) as bad_query:
                job_ads_services.create_job_add(
                    job_ad.description,
                    None,
                    'No',
                    job_ad.min_salary,
                    job_ad.max_salary,
                    job_ad.status,
                    company_id,
                    requirements,
                    requirements_levels
                )

        self.assertEqual(400, bad_query.exception.status_code)

    def test_checkCompanyExists_ReturnsTrue_IfCompany(self):
        username = 'company'
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [('random data from table',)]

            result = job_ads_services.check_company_exist(username)

        self.assertTrue(result)

    def test_checkCompanyExists_ReturnsFalse_IfNotFound(self):
        username = 'company'
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.check_company_exist(username)

        self.assertFalse(result)

    # Method is being used a lot. That is why it is tested.
    # At a future time we will move to testing for a list of objects.')
    def test_viewAllJobAds_ReturnsListWithDict(self):
        job_ad_id = 1
        status = 'status'
        now = datetime.now()
        with patch('services.job_ads_services.read_query') as read_query, \
                patch('services.job_seeker_services.get_cv_location_name') as gln, \
                patch('services.job_ads_services.get_cv_location_id') as gclid:
            gln.return_value = 'city'
            gclid.return_value = 1
            read_query.return_value = [
                (1, 'description', 1000, 2000, 'status', now)
            ]

            result = job_ads_services.view_job_ads_by_id(job_ad_id, status)

        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)
        self.assertEqual(1, result[0]['Job Ad ID'])
        self.assertEqual('description', result[0]['Job Description'])
        self.assertEqual(1000, result[0]['Minimum Salary'])
        self.assertEqual(2000, result[0]['Maximum Salary'])
        self.assertEqual('city', result[0]['Location'])
        self.assertEqual('status', result[0]['Status'])
        self.assertEqual(now, result[0]['Date Posted'])

    # This could serve as a model example for a lot of NotFound tests.
    def test_viewAllJobAds_ReturnsNoneOrRaisesException_IfNotFound(self):
        job_ad_id = 1
        status = 'status'
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            # with self.assertRaises(HTTPException) as not_found:
            #     result = job_ads_services.view_job_ads_by_id(job_ad_id, status)

            try:
                result = job_ads_services.view_job_ads_by_id(job_ad_id, status)
                self.assertIsNone(result)
            except HTTPException as not_found:
                self.assertEqual(404, not_found.status_code)

    @unittest.skip("Optional test: will be written out at future object-centred refactoring.\n"
                   "Similar to test_getJobAdAsObject_ReturnsJobAdObject")
    def test_viewJobAdsById_ReturnsJobAd(self):
        pass

    def test_currentActiveJobAd_ReturnsNumberOfJobAds(self):
        company_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [
                ('random',),('data',),('testing',),('counting',)
            ]

            result = job_ads_services.get_current_active_job_ads(company_id)

        self.assertEqual(4, result)

    # Services method needs to be renamed.
    def test_findJobAdById_ReturnsInteger(self):
        company_id = 1
        description = 'description'

        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [
                (1,)
            ]

            result = job_ads_services.find_job_ad_by_id(company_id, description)

        self.assertIsInstance(result, int)
        self.assertEqual(1, result)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_findJobAdById_ReturnsNone_IfNotFound(self):
        company_id = 1
        description = 'description'
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.find_job_ad_by_id(company_id, description)

        self.assertIsNone(result)

    def test_checkOwnerCompanyReturnsTrue_IfFound(self):
        job_ad_id = 1
        company_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [('random data from table',)]

            result = job_ads_services.check_requirement_ad_exist(job_ad_id, company_id)

        self.assertTrue(result)

    def test_checkOwnerCompanyReturnsFalse_IfNotFound(self):
        job_ad_id = 1
        company_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.check_requirement_ad_exist(job_ad_id, company_id)

        self.assertFalse(result)

    @unittest.skip("Testing for this was skipped.\n"
                   "Reason: The logic for this test is identical to the logic\n"
                   "of other similar tests that rely on a single query.\n"
                   "Importantly, we will be moving at a future point to a more\n"
                   "object-centred approach.\n"
                   "Such functions would be deprecated\n\n"
                   "Conclusion: testing for this is a waste of resources.")
    def test_checkCompanyInformation_ReturnsList(self):
        pass

    @unittest.skip('Such methods are shown in company_test.\n'
                   'It _has_ to use update_query.\n'
                   'Skipping test due to limited time resources.')
    def test_editJobAds_UsesUpdateQuery(self):
        pass

    def test_editJobAds_RaisesException_IfLevelHigherThanAdvanced(self):
        job_ad = fake_job_ad()
        job_ad_id = 1
        company_id = 1
        requirements = ['trigger']
        requirements_levels = ['4']

        with patch('services.job_ads_services.update_query') as update_query:
            update_query.return_value = None

            with self.assertRaises(HTTPException) as bad_request:
                job_ads_services.edit_job_ads(
                    company_id,
                    job_ad_id,
                    job_ad.min_salary,
                    job_ad.max_salary,
                    job_ad.description,
                    requirements,
                    requirements_levels
                )

            self.assertEqual(400, bad_request.exception.status_code)

    def test_editJobAds_RaisesSuccessfulException_WhenCompleted(self):
        job_ad = fake_job_ad()
        job_ad_id = 1
        company_id = 1
        requirements = None
        requirements_levels = None

        with patch('services.job_ads_services.update_query') as update_query:
            update_query.return_value = None

            with self.assertRaises(HTTPException) as successful:
                job_ads_services.edit_job_ads(
                    company_id,
                    job_ad_id,
                    job_ad.min_salary,
                    job_ad.max_salary,
                    job_ad.description,
                    requirements,
                    requirements_levels
                )

        self.assertEqual(200, successful.exception.status_code)

    def test_existingRequirements_ReturnsListOfRequirements(self):
        job_ad_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [
                ('python',),('java',)
            ]

            result = job_ads_services.existing_requirements(job_ad_id)

        self.assertIsInstance(result, list)

    def test_findRequirementById_ReturnsString(self):
        req_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [
                ('python',)
            ]

            result = job_ads_services.find_requirement_by_id(req_id)

        self.assertIsInstance(result, str)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_findRequirementReturnsNone_IfNotFound(self):
        req_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.find_requirement_by_id(req_id)

        self.assertIsNone(result)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_findRequirementById_ReturnsNone_WhenNotFound(self):
        skill_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.find_requirement_by_name(skill_id)

            self.assertIsNone(result)

    def test_findRequirementsLevel_ReturnsString(self):
        job_ad_id = 1
        req_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [
                ('3',)
            ]

            result = job_ads_services.find_requirements_level(job_ad_id, req_id)

        self.assertIsInstance(result, str)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_findRequirementLevel_ReturnsNone_WhenNotFound(self):
        job_ad_id = 1
        requirement_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.find_requirements_level(job_ad_id, requirement_id)

        self.assertIsNone(result)

    def test_findRequirementByName_ReturnsInteger(self):
        skill_name = 'skill'
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [
                (1,)
            ]

            result = job_ads_services.find_requirement_by_name(skill_name)

            self.assertIsInstance(result, int)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_findRequirementByName_ReturnsNone_IfNotFound(self):
        skill_name = 'skill'
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.find_requirement_by_name(skill_name)

            self.assertIsNone(result)

    def test_findRequirementByName_ReturnsTrue_WhenFound(self):
        job_ad_id = 1
        requirement_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [(1,)]

            result = job_ads_services.check_requirement_ad_exist(job_ad_id, requirement_id)

        self.assertTrue(result)

    def test_checkRequirementAdExist_ReturnsFalse_WhenNotFound(self):
        job_ad_id = 1
        requirement_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.check_requirement_ad_exist(job_ad_id, requirement_id)

        self.assertFalse(result)

    def test_convertLevelName_ReturnsCorrectInts(self):
        level = 'Beginner'
        result = job_ads_services.convert_level_name(level)
        self.assertEqual(1, result)

        level = 'Intermidiate'
        result = job_ads_services.convert_level_name(level)
        self.assertEqual(2, result)

        level = 'Advanced'
        result = job_ads_services.convert_level_name(level)
        self.assertEqual(3, result)

    def test_convertLevelName_RaisesException_InvalidInput(self):
        level = 'NotValid'

        with self.assertRaises(HTTPException) as bad_query:
            job_ads_services.convert_level_name(level)

        self.assertEqual(400, bad_query.exception.status_code)

    def test_getLevelJobAd_ReturnsString(self):
        job_ad_id = 1
        skill_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [
                ('Advanced',)
            ]

            result = job_ads_services.get_level(job_ad_id, skill_id)

            self.assertIsInstance(result, str)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_getLevelJobAd_ReturnsNone_IfNotFound(self):
        job_ad_id = 1
        skill_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.get_level(job_ad_id, skill_id)

            self.assertIsNone(result)

    # Method in services needs to be renamed to get_current_job_ads requirements
    def test_getCurrentJobAd_ReturnsCorrectlyFormattedList(self):
        job_ad_id = 1

        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [
                (1, 'python', 'advanced'),
                (2, 'java', 'beginner')
            ]

            result = job_ads_services.get_current_job_ad(job_ad_id)

        self.assertEqual('python;advanced', result[0])
        self.assertEqual('java;beginner', result[1])

    @unittest.skip('CLOSE TO IMPOSSIBLE TO TEST, needs convoluted patching.\n'
                   'The sprawling queries forced me to quit on testing.\n'
                   'Insanity ensues.')
    def test_calculatePercentageCv_ReturnsCorrectPercentages(self):
        perms = 'Seeker'
        salary_range = (1000, 2000)
        sorting = 'Best'
        with patch('services.job_ads_services.read_query') as read_query , \
                patch('services.job_ads_services.calculate_cv_salaries') as calculate_cv_salaries, \
                patch('services.job_ads_services.find_name_for_job_seeker') as fnjs_id, \
                patch('services.job_ads_services.find_username_job_seeker') as fujs, \
                patch('services.job_seeker_services.get_cv_location_name') as gcln, \
                patch('services.job_seeker_services.get_cv_location_id') as gcli, \
                patch('services.job_ads_services.get_main_cv_skills') as gmcs, \
                patch('services.job_ads_services.get_current_job_ad') as gcja, \
                patch('common.percent_jobad_calculator.find_matched') as find_matched, \
                patch('common.percent_jobad_calculator.find_unmatched') as find_unmatched, \
                patch('common.percent_jobad_calculator.percentage_calculator') as percentage_calculator:
            percentage_calculator.return_value = 100
            find_unmatched.return_value = 'Unmatched Skills'
            find_matched.return_value = 'Matched Skills'
            gmcs.return_value = 1
            gcli.return_value = 1
            gcja.return_value = 1
            gcln.return_value = 1
            fujs.return_value = 1
            fnjs_id.return_value = 1
            read_query.return_value = 1

            calculate_cv_salaries.return_value = {1: (1000, 2000)}

    def test_GetSkillName_ReturnsString(self):
        skill_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [('python',)]

            result = job_ads_services.get_skill_name(skill_id)

            self.assertIsInstance(result, str)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_GetSkillName_ReturnsNone_IfNotFound(self):
        skill_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.get_skill_name(skill_id)

            self.assertIsNone(result)

    def test_getLevel_ReturnsString(self):
        cv_id = 1
        skill_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [
                ('Advanced',)
            ]

            result = job_ads_services.get_level(cv_id, skill_id)

            self.assertIsInstance(result, str)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_getLevel_ReturnsNone_IfNotFound(self):
        cv_id = 1
        skill_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.get_level(cv_id, skill_id)

            self.assertIsNone(result)

    def test_mainCvSkills_ReturnsCorrectlyFormattedList(self):
        mini_cv_id = 1

        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [
                (1, 'python', 'advanced'),
                (2, 'java', 'beginner')
            ]

            result = job_ads_services.get_main_cv_skills(mini_cv_id)

        self.assertEqual('python;advanced', result[0])
        self.assertEqual('java;beginner', result[1])

    # Below two needs to be renamed in services and here
    def test_findNameForJobSeeker_ReturnsInteger(self):
        cv_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [(1,)]

            result = job_ads_services.find_name_for_job_seeker(cv_id)

            self.assertIsInstance(result, int)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_findNameForJobSeeker_ReturnsNone_IfNotFound(self):
        cv_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.find_name_for_job_seeker(cv_id)

            self.assertIsNone(result)

    def test_findUsernameJobSeeker_ReturnsString(self):
        job_seeker_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [
                ('username',)
            ]

            result = job_ads_services.find_username_job_seeker(job_seeker_id)

            self.assertIsInstance(result, str)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_findUsernameJobSeeker_IfNotFound(self):
        job_seeker_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.find_username_job_seeker(job_seeker_id)

            self.assertIsNone(result)

    def test_findSeekerNameCVDescriptionFromCV_ReturnsTwoStrings(self):
        cv_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [
                ('username', 'description')
            ]

            result = job_ads_services.find_seeker_name_cv_description_from_cv(cv_id)

            self.assertIsInstance(result[0][0], str)
            self.assertIsInstance(result[0][1], str)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_findSeekerNameCVDescriptionFromCV_ReturnsEmptyList_IfNotFound(self):
        cv_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.find_seeker_name_cv_description_from_cv(cv_id)

            self.assertIsNone(result)

    def test_getCvLocationId_ReturnsInteger(self):
        cv_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [(1,)]

            result = job_ads_services.get_cv_location_id(cv_id)

            self.assertIsInstance(result, int)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_getCvLocationId_ReturnsNone_IfNotFound(self):
        cv_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.get_cv_location_id(cv_id)

            self.assertIsNone(result)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_getCvLocationDirectlyById_ReturnsString(self):
        cv_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = [('City',)]

            result = job_ads_services.get_cv_location_directly_by_id(cv_id)

            self.assertIsInstance(result, str)

    @unittest.skip("Optional test: this test will be activated at more thorough bug testing")
    def test_getCvLocationDirectlyById_ReturnsNone_IfNotFound(self):
        cv_id = 1
        with patch('services.job_ads_services.read_query') as read_query:
            read_query.return_value = []

            result = job_ads_services.get_cv_location_directly_by_id(cv_id)

            self.assertIsNone(result)
