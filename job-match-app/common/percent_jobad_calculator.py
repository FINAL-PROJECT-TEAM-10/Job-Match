def job_ad_percentage_calculator(requirements, skills):

    matching_requirements = sum(skill in skills for skill in requirements)

    percentage = (matching_requirements / len(requirements)) * 100

    return percentage


#TODO: REMOVE ONE FROM THE TWO FUNCS

def find_matched(requirements , skills):
    
    matched_skills = [skill for skill in requirements if skill in skills]

    return matched_skills

def find_unmatched(requirements, skills):

    unmatched_skills = [skill for skill in requirements if skill not in skills]

    return unmatched_skills
