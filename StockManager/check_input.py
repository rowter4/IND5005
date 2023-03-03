def check_empty_field(data):
    if data == "":
        return 'blank'
    else:
        return 'ok'

def check_dtype(data, correct_dtype):
    if isinstance(data, correct_dtype):
        return 'ok'
    else:
        return 'error'

