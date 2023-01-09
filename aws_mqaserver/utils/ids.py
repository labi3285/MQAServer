import operator

def format_ids(ids):
    if len(ids) == 0:
        return None
    elif len(ids) == 1:
        return '/' + ids[0] + '/'
    else:
        return '/' + '/'.join(ids) + '/'

def get_ids(format_ids):
    if format_ids == None or len(format_ids) == 0:
        return None
    else:
        arr = []
        for e in format_ids.split("/"):
            if len(e) > 0:
                arr.append(e)
        return arr
def contains_id(id, format_ids):
    if id == None or format_ids == None:
        return False
    return operator.contains(format_ids, '/' + id + '/')

def contains_ids(fids, format_ids):
    ids = get_ids(fids)
    if ids == None:
        return False
    for id in ids:
        if contains_id(id, format_ids):
            return True
    return False




