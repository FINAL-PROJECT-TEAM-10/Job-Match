from fastapi.responses import JSONResponse
from data.database import read_query
from services import job_ads_services

def percent_section_helper(current_sort, list_of_percentages, job_ads_list): 
        
    result = []
    
    for key, value in list_of_percentages.items():
        if current_sort == 'Best' and value == 100:
            mini_cv_info = find_job_ad_info_by_id(int(key))
            mini_cv_id = find_company_id(mini_cv_info[0][0])
            result.append(create_current_dict(mini_cv_id,mini_cv_info,value))

        if current_sort == 'Very good' and 75 <= value < 100:
            mini_cv_info = find_job_ad_info_by_id(int(key))
            mini_cv_id = find_company_id(mini_cv_info[0][0])
            result.append(create_current_dict(mini_cv_id,mini_cv_info,value))

        if current_sort == 'Good' and  50 <= value < 75:
            mini_cv_info = find_job_ad_info_by_id(int(key))
            mini_cv_id = find_company_id(mini_cv_info[0][0])
            result.append(create_current_dict(mini_cv_id,mini_cv_info,value))
        
        if current_sort == 'Bad' and  26 <= value < 49:
            mini_cv_info = find_job_ad_info_by_id(int(key))
            mini_cv_id = find_company_id(mini_cv_info[0][0])
            result.append(create_current_dict(mini_cv_id,mini_cv_info,value))

        if current_sort == 'Worst' and  0 <= value < 25:
            mini_cv_info = find_job_ad_info_by_id(int(key))
            mini_cv_id = find_company_id(mini_cv_info[0][0])
            result.append(create_current_dict(mini_cv_id,mini_cv_info,value))
            
    if not result:
        return JSONResponse(status_code=404, content=f"There is no available CV'S in this section")
    
    return result


def create_current_dict(company_id, job_ad_info, value):

    return {
        "Job Seeker": find_name_by_id_for_job_seeker(company_id),
        "Description": job_ad_info[0][3],
        "Minimum Salary": job_ad_info[0][1],
        "Maximum Salary": job_ad_info[0][2],
        "Match percent based on your Company Requirements": f'{value}% / 100%'
    }


def find_job_ad_info_by_id(id:int):

    data = read_query('SELECT * FROM mini_cvs WHERE id = ?', (id,))

    return data

def find_company_id(job_ad_id):

    company_id = read_query('SELECT job_seekers_id FROM mini_cvs WHERE id = ?', (job_ad_id,))

    return company_id[0][0]

def find_name_by_id_for_job_seeker(id: int):
    data = read_query('SELECT username from job_seekers WHERE id = ?',(id,))
    return data[0][0]

#TODO Procentite trqbva da se izmislqt kum chetvurtata tablica kak shte se advat