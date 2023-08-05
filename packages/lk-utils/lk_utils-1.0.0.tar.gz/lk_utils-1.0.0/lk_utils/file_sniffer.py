from os import walk, listdir, path as ospath, environ
from sys import argv, path as syspath

from .lk_logger import lk


# ---------------------------------------------------------------- path trickers

def prettify_dir(adir: str) -> str:
    if '\\' in adir:
        adir = adir.replace('\\', '/')
    if adir[-1] != '/':
        adir += '/'
    return adir


def prettify_file(afile: str) -> str:
    if '\\' in afile:
        afile = afile.replace('\\', '/')
    return afile


def get_dirname(adir: str):
    return adir.strip('/').rsplit('/', 1)[-1]


def get_filename(file, include_postfix=True):
    file = prettify_file(file)
    if '/' not in file and '.' not in file:
        return file
    
    if '/' in file:
        filename = ospath.split(file)[1]
    else:
        filename = file
    
    if not include_postfix:
        filename = ospath.splitext(filename)[0]
    
    return filename


# ---------------------------------------------------------------- path getters

def get_lkdb_path():
    # NOTE: this is an environmental path.
    return prettify_dir(environ['LKDB'])


def get_launch_path():
    path = ospath.abspath(argv[0])
    return prettify_file(path)


def get_curr_dir() -> str:
    """
    
    IN: get_launch_path()
            获得启动文件的绝对路径, 假设为 'D:workspace/my_project/launcher.py'
    OT: 返回启动文件所在的目录
            示例: 'D:workspace/my_project/'
    
    """
    adir = ospath.split(get_launch_path())[0]
    """
    get_launch_path() = 'D:workspace/my_project/launcher.py'
    --> ospath.split(get_launch_path()) = [
            'D:workspace/my_project',
            'launcher.py'
        ]
    --> ospath.split(get_launch_path())[0] = 'D:workspace/my_project'
    """
    return prettify_dir(adir)


curr_dir = get_curr_dir()


# ---------------------------------------------------------------- path finders

def find_files(adir, postfix='', return_full_path=True):
    adir = prettify_dir(adir)
    all_files = listdir(adir)
    
    if return_full_path:
        all_files = [adir + x for x in all_files if ospath.isfile(adir + x)]
    else:
        all_files = [x for x in all_files if ospath.isfile(adir + x)]
    
    if not postfix:
        return all_files
    else:
        if isinstance(postfix, str):
            files = [x for x in all_files if postfix in x]
        else:
            '''
            注: 如果 postfix 的类型是列表或元组, 那么每个元素必须以 "." 开头, 比如:
                正确: [".mp4"]
                错误: ["mp4"]
            '''
            files = [x for x in all_files if
                     ospath.splitext(x)[1].lower() in postfix]
            # ospath.splitext(x)[1] 得到的后缀名是以 "." 开头的
        return files


def find_filenames(adir, postfix=''):
    return find_files(adir, postfix, False)


def findall_files(main_dir: str) -> list:
    collector = []
    
    for root, dirs, files in walk(main_dir):
        root = prettify_dir(root)
        collector.extend([root + f for f in files])
    
    return collector


def find_subdirs(main_dir, return_full_path=True) -> list:
    paths = listdir(main_dir)
    
    if return_full_path:
        subdirs = [main_dir + x + '/' for x in paths if
                   ospath.isdir(main_dir + x)]
    else:
        subdirs = [x for x in paths if ospath.isdir(main_dir + x)]
    
    return subdirs


def findall_subdirs(main_dir: str) -> list:
    """

    refer: https://www.cnblogs.com/bigtreei/p/9316369.html

    :param main_dir:
    :return:
    """
    collector = []
    
    for root, dirs, files in walk(main_dir):
        root = prettify_dir(root)
        collector.extend(root + d for d in dirs)
    
    return collector


def find_project_dir(custom_working_entrance=''):
    """
    注: 当从 pycharm 启动时, 项目路径就是 syspath 的第二个元素 (syspath[1]); 当从 cmd 或
    者 pyinstaller 导出后的 exe 启动时, 项目路径就是当前文件所在的路径.
    如果您想要自定义项目路径, 请在启动脚本的顶部加入此代码片段:
        # test.py
        from lk_utils import file_sniffer
        
        file_sniffer.curr_project_dir = file_sniffer.find_project_dir(
            file_sniffer.curr_dir
        )
        
        # 或者
        file_sniffer.curr_project_dir = file_sniffer.find_project_dir(
            file_sniffer.get_relpath(__file__, '.')
        )
        
    """
    if custom_working_entrance:
        p = ospath.abspath(custom_working_entrance)
        if p not in syspath:
            syspath.insert(1, p)
    
    assume_project_dir = prettify_dir(syspath[1])
    
    if assume_project_dir in curr_dir:
        """
        assume_project_dir = 'D:/likianta/workspace/myprj/'
        curr_dir = 'D:/likianta/workspace/myprj/src/'
        """
        return assume_project_dir
    else:
        return curr_dir


curr_project_dir = find_project_dir()


# ---------------------------------------------------------------- path locator

class Locator:
    # path_manager = ''
    # last_requester = ''
    
    # auto_reset = True
    
    def __init__(self):
        self.root = curr_project_dir
        self.observer = self.root
        
        self.quick_file = {
            'in'     : self.root + 'temp/in.txt',
            'in.txt' : self.root + 'temp/in.txt',
            'out'    : self.root + 'temp/out.txt',
            'out.txt': self.root + 'temp/out.txt',
        }
    
    def holdir(self, path: str):  # set observation point
        if path[-1] != '/':
            path += '/'
        lk.prt('[D1355] holdir = {}'.format(path), hierarchy=3)
        self.observer = self.root + prettify_dir(path)
    
    def release(self):  # reset observer
        lk.prt('[D1356] release holdir', hierarchy=3)
        self.observer = self.root
    
    def get(self, path):
        """
        注意:
            path 必须是相对路径.
        提示:
            传入的参数 path, 请通过 pycharm 快捷键 ctrl + alt + shift + c 获得.

        :param path: e.g. 'data/dict/deduction/irrelevant_areas.json'
        :return: 返回的是绝对路径, 所以不用担心启动文件的路径问题
        """
        return self.observer + path
    
    def quick_get(self, p):
        return self.quick_file.get(p, '')


# ---------------------------------------------------------------- quicks

def isfile(filepath: str) -> bool:
    """
    一个不是很可靠的方法, 判断是否 (看起来像是) 文件路径.
    
    与 os.path.isfile 不同的地方在于, 本方法允许使用未存在的 filepath. 换句话说, 本函数只检
    测 filepath 是不是 "看起来像" 文件, 并不保证一定能判断准确 (比如在文件夹名称中带点号就会误
    判).
    虽然本方法不能保证百分百正确, 但应对常见的情况足够了. 同时, 本方法也会尽可能保证检测的效率.
    
    如何加速判断:
        使 filepath 的字符串以 '/' 结尾
    
    """
    if ospath.exists(filepath):
        return ospath.isfile(filepath)
    
    if filepath.endswith('/'):
        return False
    elif '.' in filepath.rsplit('/', 1)[1]:
        return True
    else:
        return False


def isdir(dirpath: str) -> bool:
    if dirpath in ('.', './', '/'):
        return True
    else:
        return not isfile(dirpath)
    

def getpath(path: str):
    """
    快速地获取文件路径. 返回的是绝对路径.
    
    使用方法见 
        https://blog.csdn.net/Likianta/article/details/89299937#20190414185549
    
    注: path 参数填相对于项目根路径的路径.
    
    :param path:
    :return:
    """
    if path.startswith('../'):
        path = path.replace('../', '')
    elif path.startswith('./'):
        path = path[2:]
    # lk.logt('[TEMPRINT]', curr_project_dir)
    return curr_project_dir + path


def get_relpath(a, b):
    """
    已知绝对路径 a, 求 "相对距离" 为 b 的某一路径.

    IO: a                           | b         | out
        'D:/workspace/myprj/A/B.py' | '../'     | 'D:/workspace/myprj/'
        'D:/workspace/myprj/A/B.py' | 'C/D/'    | 'D:/workspace/myprj/A/C/D/'
        'D:/workspace/myprj/A/'     | 'C/D/'    | 'D:/workspace/myprj/A/C/D/'
        'D:/workspace/myprj/A/B.py' | '../C/D/' | 'D:/workspace/myprj/C/D/'
    """
    if isfile(a):
        a = ospath.split(a)[0]
    
    if b in ('', '.', './'):
        return prettify_dir(a)
    
    if isfile(b):
        return prettify_file(ospath.abspath(ospath.join(a, b)))
    else:
        return prettify_dir(ospath.abspath(ospath.join(a, b)))


# ---------------------------------------------------------------- interactive

def dialog(adir, postfix, prompt='请选择您所需文件的对应序号') -> str:
    """
    文件对话框.

    输入: 要查看的文件夹和该文件夹下的指定后缀的文件
    输出: 指定的文件的绝对路径
    """
    if not prompt.endswith(': '):
        prompt += ': '
    print(f'当前目录为: {adir}')
    
    files = find_files(adir, postfix, return_full_path=True)
    filenames = find_files(adir, postfix, return_full_path=False)
    
    if not filenames:
        print('[WARNING] 当前目录没有找到表格类型的文件')
        return ''
    
    elif len(filenames) == 1:
        print(f'当前目录找到了一个目标类型的文件: {filenames[0]}')
        return files[0]
    
    else:
        x = ['{} | {}'.format(i, j) for i, j in enumerate(filenames)]
        print('当前目录找到了多个目标类型的文件:\n\t{}'.format('\n\t'.join(x)))
        
        index = input(prompt)
        return files[int(index)]
