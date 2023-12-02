import unittest
from unittest.mock import patch, Mock

import services.skill_requirement_services
from services import skill_requirement_services
from app_models.skill_requirement_models import SkillRequirement

from fastapi.exceptions import HTTPException


def fake_skill():
    skill = Mock()
    skill.id = 1
    skill.name = 'skill'
    skill.description = 'description'
    skill.career_type = 'career'

    return skill


class SkillRequirementServices_Should(unittest.TestCase):
    def test_skillExistsReturnsTrue_IfSkill(self):
        skill = fake_skill()
        with patch('services.skill_requirement_services.read_query') as read_query:
            read_query.return_value = [
                (1,)
            ]

            exists = skill_requirement_services.skill_exists(skill)

        self.assertTrue(exists)

    def test_skillExistsReturnsFalse_IfSkillNotFound(self):
        skill = fake_skill()
        with patch('services.skill_requirement_services.read_query') as read_query:
            read_query.return_value = []

            exists = skill_requirement_services.skill_exists(skill)

        self.assertFalse(exists)

    def test_skillExistsById_ReturnsTrue_IfSkill(self):
        skill = fake_skill()
        with patch('services.skill_requirement_services.read_query') as read_query:
            read_query.return_value = [
                (1,)
            ]

            exists = skill_requirement_services.skill_exists_by_id(skill.id)

        self.assertTrue(exists)

    def test_skillExistsByIdReturnsFalse_IfSkillNotFound(self):
        skill = fake_skill()
        with patch('services.skill_requirement_services.read_query') as read_query:
            read_query.return_value = []

            exists = skill_requirement_services.skill_exists_by_id(skill.id)

        self.assertFalse(exists)

    def test_createSkill_returnsNewSkillId(self):
        # TODO: Would be better with an SQLite Database
        skill = fake_skill()
        with patch('services.skill_requirement_services.insert_query') as insert_query:
            insert_query.return_value = 7

            new_id = skill_requirement_services.create_skill(skill)

        self.assertIsInstance(new_id, int)
        self.assertEqual(7, new_id)

    def test_createSkillUsesInsertQuery(self):
        skill = fake_skill()
        with patch('services.skill_requirement_services.insert_query') as insert_query:
            insert_query.return_value = None

            skill_requirement_services.create_skill(skill)

        insert_query.assert_called_once()

    def test_getAllSkillsReturnsListOfSkills(self):
        with patch('services.skill_requirement_services.read_query') as read_query:
            read_query.return_value = [
                (1, 'skill1', 'description1', 'career_type1'),
                (2, 'skill2', 'description2', 'career_type2')
            ]

            skills = skill_requirement_services.get_all_skills()

        self.assertIsInstance(skills, list)
        self.assertEqual(2, len(skills))
        self.assertIsInstance(skills[0], SkillRequirement)
        self.assertEqual(2, skills[1].id)
        self.assertEqual('skill2', skills[1].name)
        self.assertEqual('description2', skills[1].description)
        self.assertEqual('career_type2', skills[1].career_type)

    def test_getAllSkillsReturnsEmptyListIfNoSkillsInDatabase(self):
        with patch('services.skill_requirement_services.read_query') as read_query:
            read_query.return_value = []

            skills = skill_requirement_services.get_all_skills()

        self.assertIsInstance(skills, list)
        self.assertEqual(0, len(skills))

    def test_getSkillByIdReturnsSkill_IfFound(self):
        skill_id = 2
        with patch('services.skill_requirement_services.read_query') as read_query:
            read_query.return_value = [
                (2, 'skill2', 'description2', 'career_type2')
            ]

            skill = skill_requirement_services.get_skill_by_id(2)

        self.assertIsInstance(skill, SkillRequirement)

    def test_getSkillByIdReturnsNone_IfSkillNotFound(self):
        skill_id = 2
        with patch('services.skill_requirement_services.read_query') as read_query:
            read_query.return_value = []

            skill = skill_requirement_services.get_skill_by_id(skill_id)

        self.assertIsNone(skill)

    def test_updateSkillUsesUpdateQuery(self):
        skill = fake_skill()
        with patch('services.skill_requirement_services.update_query') as update_query:
            update_query.return_value = None

            skill_requirement_services.update_skill(skill)

        update_query.assert_called_once()

    def test_isRequirementInJobAds_ReturnsTrueIfJobAdHasRequirement(self):
        skill = fake_skill()
        with patch('services.skill_requirement_services.read_query') as read_query:
            read_query.return_value = [
                (1,)
            ]

            exists = skill_requirement_services.is_requirement_in_job_ads(skill.id)

        self.assertTrue(exists)

    def test_isRequirementInJobAds_ReturnsFalseIfNoJobAdHasRequirement(self):
        skill = fake_skill()
        with patch('services.skill_requirement_services.read_query') as read_query:
            read_query.return_value = []

            exists = skill_requirement_services.is_requirement_in_job_ads(skill.id)

        self.assertFalse(exists)

    def test_isSkillInMiniCvs_ReturnsTrueIfJobAdHasRequirement(self):
        skill = fake_skill()
        with patch('services.skill_requirement_services.read_query') as read_query:
            read_query.return_value = [
                (1,)
            ]

            exists = skill_requirement_services.is_skill_in_mini_cvs(skill.id)

        self.assertTrue(exists)

    def test_isSkillInMiniCvs_ReturnsFalseIfNoJobAdHasRequirement(self):
        skill = fake_skill()
        with patch('services.skill_requirement_services.read_query') as read_query:
            read_query.return_value = []

            exists = skill_requirement_services.is_skill_in_mini_cvs(skill.id)

        self.assertFalse(exists)

    def test_simpleDeleteUsesUpdateQuery(self):
        skill = fake_skill()
        with patch('services.skill_requirement_services.update_query') as update_query:
            update_query.return_value = None

            skill_requirement_services.simple_delete(skill.id)

        update_query.assert_called_once()

    def test_forceDelete_UsesUpdateQueriesTransaction(self):
        skill = fake_skill()
        with patch('services.skill_requirement_services.update_queries_transaction') as uqt:
            uqt.return_value = True

            skill_requirement_services.force_delete(skill.id)

        uqt.assert_called_once()

    def test_forceDeleteRaisesConflictException_IfTransactionUnsuccessful(self):
        skill = fake_skill()
        with patch('services.skill_requirement_services.update_queries_transaction') as uqt:
            uqt.return_value = False

            with self.assertRaises(HTTPException) as conflict:
                skill_requirement_services.force_delete(skill.id)
            self.assertEqual(409, conflict.exception.status_code)


