
def uniqListOfLists(lst):
    return [list(x) for x in set(tuple(x) for x in lst)]

def flatten(lst):
    return [item for sublist in lst for item in sublist]

def uniq(lst):
    return list(set(lst))
