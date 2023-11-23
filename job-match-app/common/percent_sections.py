from fastapi.responses import JSONResponse
from data.database import read_query
from services import job_ads_services
def percent_section_helper(current_sort, list_of_percentages, perms): 
    #TODO: MAKE THE FUNCTION FRINEDLY FOR BOTH SIDES SEEKERS/COMPANIES TO ESCAPE COPY PASTE CODE
        
    result = []
    for key, value in list_of_percentages.items():
        if current_sort == 'Best' and value == 100:
            job_ad_info = find_info_by_id(int(key), perms)
            company_id = find_names(job_ad_info[0][0], perms)
            result.append(create_current_dict(company_id,job_ad_info,value, perms))

        if current_sort == 'Very good' and 75 <= value < 100:
            job_ad_info = find_info_by_id(int(key), perms)
            company_id = find_names(job_ad_info[0][0], perms)
            result.append(create_current_dict(company_id,job_ad_info,value, perms))

        if current_sort == 'Good' and  50 <= value < 75:
            job_ad_info = find_info_by_id(int(key), perms)
            company_id = find_names(job_ad_info[0][0], perms)
            result.append(create_current_dict(company_id,job_ad_info,value, perms))
        
        if current_sort == 'Bad' and  26 <= value < 49:
            job_ad_info = find_info_by_id(int(key), perms)
            company_id = find_names(job_ad_info[0][0], perms)
            result.append(create_current_dict(company_id,job_ad_info,value, perms))

        if current_sort == 'Worst' and  0 <= value < 25:
            job_ad_info = find_info_by_id(int(key), perms)
            company_id = find_names(job_ad_info[0][0], perms)
            result.append(create_current_dict(company_id,job_ad_info,value, perms))

# Best - 100%
# Very Good - 75% - 99%
# Good - 50% - 74%
# Bad - 49% - 26%
# Worst - 25% - 0%

            
    if not result:
        return JSONResponse(status_code=404, content=f'There is no available job ads in this section')
    
    return result


def create_current_dict(company_id, job_ad_info, value, perms):
    if perms == 'Seeker':
        return {
            "Company": job_ads_services.find_name_by_id(company_id),
            "Description": job_ad_info[0][1],
            "Minimum Salary": job_ad_info[0][2],
            "Maximum Salary": job_ad_info[0][3],
            "Match percent based on your CV skills": f'{value}% / 100%',
        }
    else:
        return {
            "Job Seeker": find_names(company_id),
            "Description": job_ad_info[0][3],
            "Minimum Salary": job_ad_info[0][1],
            "Maximum Salary": job_ad_info[0][2],
            "Match percent based on your Company Requirements": f'{value}% / 100%'
    }


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
        data = read_query('SELECT job_seekers_id from mini_cvs WHERE id = ?', (id, ))

    return data[0][0]

def find_name_by_id_for_job_seeker(id: int):
    data = read_query('SELECT username from job_seekers WHERE id = ?',(id,))
    return data[0][0]