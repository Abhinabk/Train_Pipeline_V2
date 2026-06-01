import re


def normalize_names(name:str)->str:
    '''Use UPPER CASE FOR ALL, strips JN/JUNCTION '''
    n = name.upper().strip()
    n = re.sub(r'\s+(JN|JUNCTION)$','',n) # $ represents the end of a string  so JN but only at end
    return n
