def calculate_salaries(job_ads_info):

    result = []
    for job_ad in job_ads_info:
        current_job_range = []
        current_job_range.append(job_ad[2])
        current_job_range.append(job_ad[3]) #[3000, 5000]
        threshold_result = calculate_treshold(current_job_range)

        data_dict = {
            job_ad[0]: threshold_result,
        }
        result.append(data_dict)
    
    return result


def calculate_treshold(job_range):
    threshold_percent = 20

    min_salary, max_salary = job_range
    threshold_amount_lower = min_salary * (threshold_percent / 100)
    threshold_amount_upper = max_salary * (threshold_percent / 100)
    
    new_min_salary = min_salary - threshold_amount_lower
    new_max_salary = max_salary + threshold_amount_upper
    
    return new_min_salary, new_max_salary