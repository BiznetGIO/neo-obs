def isint(number):
    try:
        to_float = float(number)
        to_int = int(to_float)
    except ValueError:
        return False
    else:
        return to_float == to_int


def isfloat(number):
    try:
        float(number)
    except ValueError:
        return False
    else:
        return True

def get_index(dictionary):
    return [key for (key, value) in dictionary.items()]