from fastapi.responses import JSONResponse
from data.database import read_query
from services import job_seeker_services, job_ads_services

def percent_section_helper(current_sort, list_of_percentages, perms, matched_skills, unmatched_skills): 

    result = []
    for key, value in list_of_percentages.items():
        if current_sort == 'Best' and value == 100:
            job_ad_info = find_info_by_id(int(key), perms)
            company_id = find_names(job_ad_info[0][0], perms)
            skills_matched_ad = matched_skills[key]
            result.append(create_current_dict(company_id,job_ad_info,value, perms, skills_matched_ad))

        if current_sort == 'Very good' and 75 <= value < 100:
            job_ad_info = find_info_by_id(int(key), perms)
            company_id = find_names(job_ad_info[0][0], perms)
            skills_matched_ad = matched_skills[key]
            skills_unmatched_ad = unmatched_skills[key]
            result.append(create_current_dict(company_id,job_ad_info,value, perms, skills_matched_ad, skills_unmatched_ad))

        if current_sort == 'Good' and  50 <= value < 75:
            job_ad_info = find_info_by_id(int(key), perms)
            company_id = find_names(job_ad_info[0][0], perms)
            skills_matched_ad = matched_skills[key]
            skills_unmatched_ad = unmatched_skills[key]
            result.append(create_current_dict(company_id,job_ad_info,value, perms, skills_matched_ad, skills_unmatched_ad))
        
        if current_sort == 'Bad' and  25 <= value < 49:
            job_ad_info = find_info_by_id(int(key), perms)
            company_id = find_names(job_ad_info[0][0], perms)
            skills_matched_ad = matched_skills[key]
            skills_unmatched_ad = unmatched_skills[key]
            result.append(create_current_dict(company_id,job_ad_info,value, perms, skills_matched_ad, skills_unmatched_ad))

        if current_sort == 'Worst' and  0 <= value < 24:
            job_ad_info = find_info_by_id(int(key), perms)
            company_id = find_names(job_ad_info[0][0], perms)
            skills_matched_ad = matched_skills[key]
            skills_unmatched_ad = unmatched_skills[key]
            result.append(create_current_dict(company_id,job_ad_info,value, perms, skills_matched_ad, skills_unmatched_ad))
            
    if perms == 'Seeker':        
        if not result:
            return JSONResponse(status_code=404, content=f'There is no available Job Ads in this section')
    else:
        if not result:
            return JSONResponse(status_code=404, content=f'There is no available CVS in this section')
    
    return result


def create_current_dict(company_id, job_ad_info, value, perms, matched_skills, unmatched_skills = None):
    from services import job_ads_services
    matched_skills_result = []
    unmatched_skills_result = []
    if matched_skills:
        for pair in matched_skills:
            skill, level = pair.split(';')
            matched_skills_result.append(f'{skill.capitalize()} ({level.capitalize()})')
    if unmatched_skills:
        for pair in unmatched_skills:
            skill, level = pair.split(';')
            unmatched_skills_result.append(f'{skill.capitalize()} ({level.capitalize()})')

    if not matched_skills_result:
        matched_skills_result = 'No matched skills'
    else:
        matched_skills_result = ' | '.join(matched_skills_result)
        
    if not unmatched_skills_result:
        unmatched_skills_result = 'You meet all the requirements!'
    else:
        unmatched_skills_result = ' | '.join(unmatched_skills_result)

    if perms == 'Seeker':
        result_dict = {
            'Job AD ID': job_ad_info[0][0],
            "Company": job_ads_services.find_name_by_id(company_id),
            "Description": job_ad_info[0][1],
            "Minimum Salary": job_ad_info[0][2],
            "Maximum Salary": job_ad_info[0][3],
            "Prefered Location": job_seeker_services.get_cv_location_name(job_ads_services.get_cv_location_id([0])),
            "Match percent based on your CV skills": f'{value}% / 100%',
            "Matched Skills from the Company Job AD": matched_skills_result,
            "Not matched Skills": unmatched_skills_result,
        }
        return result_dict
    else:
        result_cv = {
            "Job Seeker": find_name_by_id_for_job_seeker(company_id),
            "CV Description": job_ad_info[0][3],
            "Minimum Salary": job_ad_info[0][1],
            "Maximum Salary": job_ad_info[0][2],
            "Prefered Location": job_seeker_services.get_cv_location_name(job_seeker_services.get_cv_location_id([0])),
            "Match percent based on your Company Requirements": f'{value}% / 100%',
            "Matched Requirements from the Seeker CV": matched_skills_result,
            "Not matched Requirements": unmatched_skills_result
        }
        return result_cv

def find_info_by_id(id:int, perms: str):
    if perms == 'Seeker':
        data = read_query('SELECT * FROM job_ads WHERE id = ?', (id,))
    else:
        data = read_query('SELECT * FROM mini_cvs WHERE id = ?', (id,))
    return data

def find_names(id, perms: str):
    if perms == 'Seeker':
        data = read_query('SELECT companies_id FROM job_ads WHERE id = ?', (id,))
    else:
        data = read_query('SELECT job_seekers_id from mini_cvs WHERE id = ?', (id,))

    return data[0][0]

def find_name_by_id_for_job_seeker(id: int):
    data = read_query('SELECT username from job_seekers WHERE id = ?',(id,))
    return data[0][0]

# Graph of percent calculations
# --------------
# Best - 100%
# Very Good - 75% - 99%
# Good - 50% - 74%
# Bad - 49% - 26%
# Worst - 25% - 0%