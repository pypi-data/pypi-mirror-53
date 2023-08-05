from re import compile


def get_hanz():
    return r'[\u4e00-\u9fa5]'


# ------------------------------------------------

def get_hanz_regex(single_char=False):
    if single_char:
        reg = compile(r'[\u4e00-\u9fa5]')
    else:
        reg = compile(r'[\u4e00-\u9fa5]+')
    return reg
