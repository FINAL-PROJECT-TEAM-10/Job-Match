def recognize_status(status: int):

    result =''

    if status is not 1:
        result = 'Active'
    else:
        result = 'Busy'


    return result        