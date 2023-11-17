from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app_models.skill_requirement_models import SkillRequirement
from common.auth import get_current_user
from services import skill_requirement_services

skills_router = APIRouter(prefix='/skill-requirements',
                          tags={'Skills and requirements'})


# TODO: Add filtration/pagination for skills
@skills_router.get('/')
def find_all_skills():
    skill_list = skill_requirement_services.get_all_skills()

    if skill_list == 0:
        return JSONResponse(status_code=404,
                            content='No skills/requirements found.')
    else:
        return skill_list


@skills_router.post('/', description='Admin endpoint')
def add_skill(name: str, description: str = None, career_type: str = None,
              current_user_payload=Depends(get_current_user)):
    if current_user_payload['group'] != 'admins':
        return JSONResponse(status_code=403,
                            content='Only admins can add skills/requirements.')

    skill = SkillRequirement(name=name, description=description, career_type=career_type)
    if skill_requirement_services.skill_exists(skill):
        return JSONResponse(status_code=409,
                            content=f'Skill/Requirement with name {skill.name} already exists.')

    skill.id = skill_requirement_services.create_skill(skill)

    return skill


@skills_router.get('/{id}')
def find_skill_by_id(id: int):
    skill = skill_requirement_services.get_skill_by_id(id)
    if skill:
        return skill
    else:
        return JSONResponse(status_code=404,
                            content=f'Skill/Requirement with ID#{id} was not found.')


@skills_router.put('/{id}', description='Admin endpoint')
def change_skill_name_description_and_career(id: int, name: str = None, description: str = None,
                                             career_type: str = None,
                                             current_user_payload=Depends(get_current_user)):
    if current_user_payload['group'] != 'admins':
        return JSONResponse(status_code=403,
                            content='Only admins can edit skills/requirements.')

    old_skill = skill_requirement_services.get_skill_by_id(id)
    if old_skill is None:
        return JSONResponse(status_code=404,
                            content='No such skill or requirement.')

    try:
        updated_skill = SkillRequirement(id=old_skill.id,
                                         name=name or old_skill.name,
                                         description=description or old_skill.description,
                                         career_type=career_type or old_skill.career_type)
    except ValidationError as e:
        return JSONResponse(status_code=500,
                            content=f'Skill/Requirement could not be updated. Error: {e}')

    skill_requirement_services.update_skill(updated_skill)
    return JSONResponse(status_code=200,
                        content='Skill/Requirement successfully updated.')


# TODO: Consider what happens with percent matches when force delete is called:
#  Possible solution. Forcing an update of matches that have the skill/requirement.
@skills_router.delete('/{id}', description='Admin endpoint')
def delete_skill_requirement(id: int, current_user_payload=Depends(get_current_user)):
    if current_user_payload['group'] != 'admins':
        return JSONResponse(status_code=403,
                            content='Only admins can delete skills/requirements.')

    if not skill_requirement_services.skill_exists_by_id(id):
        return JSONResponse(status_code=404,
                            content=f'No skill/requirement with ID #{id} exists.')

    skill_in_mini_cvs = skill_requirement_services.is_skill_in_mini_cvs(id)
    requirement_in_job_ads = skill_requirement_services.is_requirement_in_job_ads(id)

    if skill_in_mini_cvs or requirement_in_job_ads:
        return JSONResponse(status_code=403,
                            content=f'Skill/requirement cannot be deleted because CVs or Job Ads depend on it. '
                                    f'If you would like to delete a skill/requirement completely from the database, '
                                    f'please use FORCE DELETE. Note: force delete may make some matches obsolete.')

    skill_requirement_services.simple_delete(id)

    return JSONResponse(status_code=200,
                        content='Unused skill/requirement deleted from the database.')


@skills_router.delete('/{id}/force_delete', description='Admin endpoint')
def force_delete_skill_requirement(id: int):
    pass
