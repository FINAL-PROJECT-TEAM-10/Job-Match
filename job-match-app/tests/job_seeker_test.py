import unittest

from unittest.mock import Mock, patch

from services import job_seeker_services


class JobSeekerService_Should(unittest.TestCase):
    @unittest.skip('Logic is duplicate to logic of job_ads_test.\n'
                   'It is a logic that will be removed from future iterations of the app.\n'
                   'As we move to a closer to OOP approach.')
    def test_anything(self):
        pass