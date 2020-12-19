def try_parse_float(value):
    try:
        return float(value), True
    except ValueError:
        return None, False

def try_parse_string(value):
    try:
        v = str(value).strip(' ').lower()
        if v != '':
            return v, True
        else:
            return None, False
    except ValueError:
        return None, False