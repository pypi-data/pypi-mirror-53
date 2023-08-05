from json import dumps, loads
from json.decoder import JSONDecodeError
from os import remove
from os.path import abspath, exists as os_exists, getsize

from .lk_logger import lk


class FileSword:
    """
    基本操作:
        创建对象:
            file = FileSword('../data/sample.txt')  # 传入要读取的文件路径
        以指定文件模式 (如只读模式) 创建对象:
            file = FileSword('../data/sample.txt', mode='r')
            # 注: 默认打开模式为'a+'
        判断文件中是否含有内容 (支持大文件的快速判断):
            result = file.has_content()
        读取文本:
            contents = file.read()
        逐行读取文本 (返回一个列表):
            contents = file.read_by_line()
        写入文件:
            file.write('hello world')
        写入列表 (默认以换行符分隔):
            file.write(['1st Apple', '2nd Orange', '3rd Banana'])
        获取文本一共有多少行 (支持大文件的读取):
            line_num = file.get_num_of_lines()

    进阶操作:
        创建文件, 如果所属文件夹不存在, 则连同上级路径也创建:
            file = FileSword('../data/sample.txt', is_create_dir=True)
        创建文件, 如果该文件已存在且文件里面已有内容, 则清空已有内容:
            file = FileSword('../data/sample.txt',
            clear_any_existed_content=True)
            # 注意: 在读取模式 (mode='r') 使用此命令会引发错误
        虽然在打开时是 'a' 模式, 但是想在写入文件时临时变更为 'w' 模式:
            file = FileSword('../data/sample.txt', mode='a')
            file.write('hello world', mode='w')
        虽然在打开时是 'a' 模式, 但是想在写入文件时用 'w' 模式, 且以后都为 'w' 模式:
            file = FileSword('../data/sample.txt', mode='a')
            file.write('hello world', mode='w', conserve_mode=True)
        在写入列表时, 想要指定 '\t' 为元素分隔符:
            file.write(['1st Apple', '2nd Orange', '3rd Banana'], adhesion='\t')
        想要正式地变更文件模式:
            file = FileSword('../data/sample.txt', mode='a')
            file.change_mode('r')

    """
    file = None
    filepath = ''
    nlines = -1
    contents = []
    
    def __init__(self, path, mode='a', clear_any_existed_content=False):
        if not path:
            raise AttributeError
        
        if clear_any_existed_content and mode not in 'w+' and is_empty(path):
            """
            要清空文件中的已有内容, 需满足以下判断条件:
            1. 此文件是已存在的 (如果不存在, 就没必要去清空了)
            2. 此文件的读写模式不是 'w' 或 'w+' (如果是的话, 在写的时候就能覆盖, 自然也没必
            要去清空了)
            """
            remove(path)
            lk.logt('[D0026]', 'clear existed content ok', path, h='parent')
        
        self.filepath = path
        self.file = open(path, encoding='utf-8', mode=mode)
        self.reset_cursor()
    
    def get_file_path(self, relative=True):
        if relative:
            return self.filepath
        else:
            return abspath(self.filepath)
    
    def reset_cursor(self):
        if self.file.mode != 'r':
            """
            python - How to read from file opened in "a+" mode? - Stack Overflow
            https://stackoverflow.com/questions/14639936/how-to-read-from-file
            -opened-in-a-mode
            """
            self.file.seek(0)
    
    # ----------------------------------------------------------------
    
    def read(self):
        self.reset_cursor()
        contents = self.file.read()
        return contents
    
    def read_by_line(self, force_refresh=False):
        if not self.contents or force_refresh:
            self.contents.clear()
            self.reset_cursor()
            for line in self.file:
                self.contents.append(line.strip())
        return self.contents
    
    def has_content(self):
        return is_empty(self.filepath)
    
    def get_num_of_lines(self):
        if self.nlines >= 0:
            return self.nlines
        elif self.contents:
            return len(self.contents)
        else:
            # 支持统计超大文件行数
            # 参考: https://blog.csdn.net/sethcss/article/details/72954754
            self.reset_cursor()
            # noinspection PyUnusedLocal
            self.nlines = len(["" for line in self.file])
            return self.nlines
    
    # ----------------------------------------------------------------
    
    def write(self, contents, mode='', conserve_mode=False, adhesion='\n'):
        if isinstance(contents, list) or isinstance(contents, tuple):
            contents = map(str, contents)
            contents = adhesion.join(contents)
        
        mode_select = {
            'a+': ['a+', 'a', 'r'],
            'r+': ['r+', 'r', 'w'],
            'w+': ['w+', 'w', 'r'],
        }
        
        if mode and mode not in mode_select.get(self.file.mode, self.file.mode):
            if self.file.mode in 'w+' and mode in 'a+':
                contents += self.read()
            
            if conserve_mode:
                self.drop(new_mode=mode)
            else:
                self.drop(new_mode=self.file.mode)
        
        self.file.write(contents + '\n')
    
    # ----------------------------------------------------------------
    
    def change_mode(self, mode):
        if mode != self.file.mode:
            self.file.close()
            self.__init__(self.file.name, mode=mode)
    
    def drop(self, new_mode='a'):
        self.file.close()
        remove(self.file.name)
        self.__init__(self.file.name, mode=new_mode)
    
    def close(self):
        lk.logt('[I0058]', f'text file saved to "{self.filepath}"', h='parent')
        self.file.close()


# ----------------------------------------------------------------


def get_num_of_lines(filepath):
    """
    该方法可以高效地读取文件一共有多少行, 支持大文件的读取.

    python 统计文件行数 - CSDN博客 https://blog.csdn.net/qq_29422251/article
    /details/77713741
    """
    # noinspection PyUnusedLocal
    return len(["" for line in open(filepath, mode='r')])


def is_empty(filepath):
    """
    OT: bool.
        True: file has content.
        False: file is empty.
    """
    # https://www.imooc.com/wenda/detail/350036?block_id=tuijian_yw
    return bool(os_exists(filepath) and getsize(filepath))


# ----------------------------------------------------------------

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        contents = f.read()
        
        # https://blog.csdn.net/liu_xzhen/article/details/79563782
        if contents.startswith(u'\ufeff'):
            lk.logt('[I0135]', 'stripping BOM charset at the start of contents',
                    h='parent')
            contents = contents.encode('utf8')[3:].decode('utf8')
    
    return contents


def read_file_by_line(path, offset=0):
    """
    IN: path: str. e.g. 'test.txt'
        offset: int.
            0: 表示返回完整的列表
            n: 传一个大于 0 的数字, 表示返回 list[n:]. (ps: 如果该数字大于列表的长度,
            python 会返回一个空列表, 不会报错)
    OT: list<str>. e.g. ['aaa', 'bbb', 'ccc', ...]
    """
    # https://blog.csdn.net/qq_40925239/article/details/81486637?utm_source
    # =blogxgwz7
    with open(path, 'r', encoding='utf-8-sig') as file:
        out = [line.strip('\n') for line in file]
    return out[offset:]


def write_file(contents, filepath, mode='w', adhesion='\n'):
    """
    写入文件, 传入内容 (参数1) 可以是字符串, 也可以是数组.

    注意：
        contents = ['aaa', 'bbb', 'ccc']
        path = '../output/output.txt'
        # 不建议以下用法：
        for i in contents:
            read_and_write_basic.write_file(i, path)
        # 建议改为：
        read_and_write_basic.write_file(contents, path)

    参数:
        contents: 需要写入的文本, 可以是字符串, 也可以是数组. 传入数组时, 会自动将它转换为
        "\n" 拼接的文本
        filepath: 写入的路径, 建议使用相对路径
        mode: 写入模式, 有三种可选:
            [a] 增量写入 (默认是 [a])
            [w] 清空原内容后写入
            [wb] 在 [w] 的基础上以比特流的形式写入
        adhesion: 拼接方式, 只有当 content 为列表时会用到, 用于将列表转换为文本时选择的拼接
        方式, 默认是以 "\n" 拼接
            e.g. content = adhesion.join(content)
            # ['a', 'b', 'c'] --> 'a\nb\nc'

    参考:
        python 在最后一行追加 - 张乐乐章 - 博客园 https://www.cnblogs.com/zle1992/p
        /6138125.html
        python map https://blog.csdn.net/yongh701/article/details/50283689
    """
    if not isinstance(contents, str):
        contents = map(str, contents)
        contents = adhesion.join(contents)
        '''
        注: 暂不支持对二维数组操作, 如果 contents 的形式为:
            contents = [[1, 2, 3], [4, 5, 6]]
        请使用 write_multi_list(contents)
        '''
    
    with open(filepath, encoding='utf-8', mode=mode) as f:
        f.write(contents + '\n')


# ----------------------------------------------------------------

jsondata_singleton = {}


def read_json(path) -> dict:
    if path not in jsondata_singleton:
        try:
            jsondata = loads(read_file(path))
            jsondata_singleton[path] = jsondata
            return jsondata
        except JSONDecodeError:
            lk.logt('[E0206]', 'json decode error', path, h='parent')
            raise JSONDecodeError
    else:
        return jsondata_singleton[path]


def write_json(data, path: str):
    """
    refer:
        json.dumps 如何输出中文:
        https://www.cnblogs.com/zdz8207/p/python_learn_note_26.html
    """
    assert '.json' in path and isinstance(data, (dict, list, tuple))
    with open(path, encoding='utf-8', mode='w') as f:
        f.write(dumps(data, ensure_ascii=False))


# ---------------------------------------------------------------- 

def write_multi_list(path: str, *mlist):
    """
    refer:
        数组 (矩阵) 转置 https://blog.csdn.net/yongh701/article/details/50283689
    """
    transposited_list = zip(*mlist)
    # [[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> ((1, 4, 7), (2, 5, 8), (3, 6, 9))
    
    contents = ['\t'.join(map(str, x)) for x in transposited_list]
    # -> [('1', '4', '7'), ('2', '5', '8'), ('3', '6', '9')]
    # -> ['1\t4\t7', '2\t5\t8', '3\t6\t9']
    
    write_file(contents, path)
