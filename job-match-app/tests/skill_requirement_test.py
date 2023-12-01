import unittest
from unittest.mock import patch

from services import skill_requirement_services
from app_models.skill_requirement_models import SkillRequirement

class SkillRequirementServices_Should(unittest.TestCase):
    def test_skillExistsReturnsTrue_IfSkill(self):
        pass

    def test_skillExistsReturnsFalse_IfSkillNotFound(self):
        pass

    def test_skillExistsById_ReturnsTrue_IfSkill(self):
        pass

    def test_skillExistsByIdReturnsFalse_IfSkillNotFound(self):
        pass

    def test_createSkill_returnsNewSkillId(self):
        pass

    def test_createSkillUsesInsertQuery(self):
        pass

    def test_getAllSkillsReturnsListOfSkills(self):
        pass

    def test_getAllSkillsReturnsEmptyListIfNoSkillsInDatabase(self):
        pass

    def test_getSkillByIdReturnsSkill_IfFound(self):
        pass

    def test_getSkillByIdReturnsEmptyList_IfSkillNotFound(self):
        pass

    def test_updateSkillUsesUpdateQuery(self):
        pass

    def test_isRequirementInJobAds_ReturnsTrueIfJobAdHasRequirement(self):
        pass

    def test_isRequirementInJobAds_ReturnsFalseIfNoJobAdHasRequirement(self):
        pass

    def test_isSkillInMiniCvs_ReturnsTrueIfJobAdHasRequirement(self):
        pass

    def test_isSkillInMiniCvs_ReturnsFalseIfNoJobAdHasRequirement(self):
        pass

    def test_simpleDeleteUsesUpdateQuery(self):
        pass

    def test_forceDelete_UsesUpdateQueriesTransaction(self):
        pass

    def test_forceDeleteRaisesException_IfTransactionUnsuccessful(self):
        pass