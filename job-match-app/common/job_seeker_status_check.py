def recognize_status(status: int):

    result =''

    if status != 1:
        result = 'Active'
    else:
        result = 'Busy'


    return result


def convert_status(status: str):

    result =''

    if status == 'Active':
        result = 1
    elif status == 'Busy':
        result = 0
    else:
        result = None 


    return result   