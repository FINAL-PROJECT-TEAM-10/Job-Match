
def parse_skills(skills_str: str):

    separators = [',', '|', ' ', '.','-']

    for separator in separators:
        if separator in skills_str:
            return skills_str.split(separator)
    return skills_str.split(',')