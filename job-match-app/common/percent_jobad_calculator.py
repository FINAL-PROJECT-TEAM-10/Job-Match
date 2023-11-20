def job_ad_percentage_calculator(requirements, skills):

    matching_requirements = sum(skill in skills for skill in requirements)

    percentage = (matching_requirements / len(requirements)) * 100

    return percentage


#TODO: REMOVE ONE FROM THE TWO FUNCS
