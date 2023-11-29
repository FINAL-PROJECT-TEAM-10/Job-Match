def calculate_salaries(job_ads_info):

    result = []
    for job_ad in job_ads_info:
        current_job_range = []
        current_job_range.append(job_ad[2])
        current_job_range.append(job_ad[3])
        threshold_result = calculate_threshold(current_job_range)

        data_dict = {
            job_ad[0]: threshold_result,
        }
        result.append(data_dict)
    
    return result


def calculate_cv_salaries(cv_info, threshold_percent):
    
    result = []
    for cv in cv_info:
        cv_range = []
        cv_range.append(cv[1])
        cv_range.append(cv[2])
        threshold_result = calculate_threshold(cv_range, threshold_percent)

        data_dict = {
            cv[0]: threshold_result,
        }
        result.append(data_dict)
    
    return result

def calculate_threshold(job_range, threshold_percent):

    min_salary, max_salary = job_range
    threshold_amount_lower = min_salary * (threshold_percent / 100)
    threshold_amount_upper = max_salary * (threshold_percent / 100)
    
    new_min_salary = min_salary - threshold_amount_lower
    new_max_salary = max_salary + threshold_amount_upper
    
    return new_min_salary, new_max_salary