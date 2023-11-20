#TODO preizpolzva se kod trqbwa da se reshi koi da se mahne
def cv_percentage_calculator(requirements, skills):

    matching_requirements = sum(skill in skills for skill in requirements)

    percentage = (matching_requirements / len(requirements)) * 100

    return percentage