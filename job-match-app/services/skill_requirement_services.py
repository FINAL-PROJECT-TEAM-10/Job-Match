from app_models.skill_requirement_models import SkillRequirement
from data.database import read_query, insert_query, update_query


def skill_exists(skill: SkillRequirement) -> bool:
    return any(read_query('''SELECT id from skills_or_requirements WHERE name = ?''',
                          (skill.name,)))


def skill_exists_by_id(id: int) -> bool:
    return any(read_query('''SELECT id from skills_or_requirements WHERE id = ?''',
                          (id,)))


def create_skill(skill: SkillRequirement):
    new_skill_id = insert_query('''
    INSERT INTO skills_or_requirements (name, description, career_type)
    VALUES (?,?,?)
    ''', (skill.name, skill.description, skill.career_type))

    return new_skill_id


def get_all_skills():
    skill_data = read_query('''SELECT * FROM skills_or_requirements''')

    return (SkillRequirement.from_query_results(*row) for row in skill_data)


def get_skill_by_id(id: int):
    skill_data = read_query('''
    SELECT id, name, description, career_type FROM skills_or_requirements WHERE id = ?
    ''', (id,))

    return next((SkillRequirement.from_query_results(*row) for row in skill_data), None)


def update_skill(skill: SkillRequirement):
    return update_query('''
    UPDATE skills_or_requirements SET name = ?, description = ?, career_type = ?
    WHERE id = ?
    ''', (skill.name, skill.description, skill.career_type, skill.id))


def is_requirement_in_job_ads(id):
    return any(read_query('''
    SELECT skills_or_requirements_id FROM job_ads_has_requirements WHERE skills_or_requirements_id = ?
    ''', (id,)))


def is_skill_in_mini_cvs(id):
    return any(read_query('''
    SELECT skills_or_requirements_id FROM mini_cvs_has_skills WHERE skills_or_requirements_id = ?
    ''', (id,)))


def simple_delete(id):
    return update_query('''DELETE FROM skills_or_requirements WHERE id = ?''',
                        (id,))
