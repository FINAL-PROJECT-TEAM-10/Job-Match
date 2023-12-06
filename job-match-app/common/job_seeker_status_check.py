
def recognize_status(status: int):

    result =''

    if status != 1:
        result = 'Busy'
    else:
        result = 'Active'

    return result