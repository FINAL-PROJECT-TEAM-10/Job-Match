from fastapi.responses import JSONResponse
from data.database import read_query
from services import job_ads_services
def percent_section_helper(current_sort, list_of_percentages, job_ads_list): 

        
    result = []
    for key, value in list_of_percentages.items():
        if current_sort == 'Best' and value == 100:
            job_ad_info = find_job_ad_info_by_id(int(key))
            company_id = find_company_id(job_ad_info[0][0])
            result.append(create_current_dict(company_id,job_ad_info,value))

        if current_sort == 'Very good' and 75 <= value < 100:
            job_ad_info = find_job_ad_info_by_id(int(key))
            company_id = find_company_id(job_ad_info[0][0])
            result.append(create_current_dict(company_id,job_ad_info,value))

        if current_sort == 'Good' and  50 <= value < 75:
            job_ad_info = find_job_ad_info_by_id(int(key))
            company_id = find_company_id(job_ad_info[0][0])
            result.append(create_current_dict(company_id,job_ad_info,value))
        
        if current_sort == 'Bad' and  26 <= value < 49:
            job_ad_info = find_job_ad_info_by_id(int(key))
            company_id = find_company_id(job_ad_info[0][0])
            result.append(create_current_dict(company_id,job_ad_info,value))

        if current_sort == 'Worst' and  0 <= value < 25:
            job_ad_info = find_job_ad_info_by_id(int(key))
            company_id = find_company_id(job_ad_info[0][0])
            result.append(create_current_dict(company_id,job_ad_info,value))
            
    if not result:
        return JSONResponse(status_code=404, content=f'There is no available job ads in this section')
    
    return result


def create_current_dict(company_id, job_ad_info, value):
    return {
        "Company": job_ads_services.find_name_by_id(company_id),
        "Description": job_ad_info[0][1],
        "Minimum Salary": job_ad_info[0][2],
        "Maximum Salary": job_ad_info[0][3],
        "Match percent based on your CV skills": f'{value}% / 100%'
    }


def find_job_ad_info_by_id(id:int):

    data = read_query('SELECT * FROM job_ads WHERE id = ?', (id,))

    return data

def find_company_id(job_ad_id):

    company_id = read_query('SELECT companies_id FROM job_ads WHERE id = ?', (job_ad_id,))

    return company_id[0][0]