import time
from os import stat


def generate_timestamp(style='y-m-d h:n:s', ctime=0.0) -> str:
    """
    生成时间戳.
    
    输入: 'y-m-d h:n:s'
    输出: '2018-12-27 15:13:45'
    
    转换关系:
        year  : %Y
        month : %m
        day   : %d
        hour  : %H
        minute: %M
        second: %S
    
    注:
        目前仅支持补零数字, 比如6月2日, 会生成为 "06-02"
    """
    
    if not ctime:
        ctime = time.time()
    ctime = time.localtime(ctime)
    
    style = style \
        .replace('y', '%Y').replace('m', '%m').replace('d', '%d') \
        .replace('h', '%H').replace('n', '%M').replace('s', '%S')
    
    time_stamp = time.strftime(style, ctime)
    
    return time_stamp


def seconds_to_hms(second: int):
    """
    将秒数转换成 hms 格式.

    https://www.jb51.net/article/147479.htm
    """
    m, s = divmod(second, 60)
    h, m = divmod(m, 60)
    hms = "%02d%02d%02d" % (h, m, s)
    return hms


def get_file_modified_time(filepath, style='y-m-d h:n:s'):
    """
    demos/os_demo#get_file_created_time
    """
    time_float = stat(filepath).st_mtime
    if style == '' or style == 'float':
        return time_float
    else:
        return generate_timestamp(style, time_float)


def get_file_created_time(filepath, style='y-m-d h:n:s'):
    """
    demos/os_demo#get_file_created_time
    """
    time_float = stat(filepath).st_ctime
    if style == '' or style == 'float':
        return time_float
    else:
        return generate_timestamp(style, time_float)
