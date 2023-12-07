import unittest

from unittest.mock import Mock, patch

from services import job_seeker_matching_services


class JobSeekerMatchingService_Should(unittest.TestCase):
    @unittest.skip('Logic is almost identical to company_matching_test.\n'
                   'A lot of the methods will be removed from future iterations of the app.\n'
                   'As we move to a closer to OOP approach.')
    def test_anything(self):
        pass