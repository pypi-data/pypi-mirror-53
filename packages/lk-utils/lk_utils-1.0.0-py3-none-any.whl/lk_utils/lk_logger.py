import re
import sys
from ast import iter_child_nodes, parse as ast_parse
from inspect import stack
from os.path import abspath, relpath, split as splitpath
from time import time

from .time_utils import generate_timestamp

"""
待更新:
    增加打印风格配置, 例如不打印所属的函数等
    将 base_print() 的 prefix 设置为定宽
    设定 tag 的打印阈值, 例如凡是 Debug 级别的不打印
    支持 tag 打印时的高亮显示, 并设定高亮颜色
    增加动态抹除的进度条显示方法
    
维护事项:
    - MsgRecorder.show_important_messages() 中会跳过 '[TEMPRINT]' 这个 tag 的
    detail info, 该 tag 与 live template - lktp 相关, 如有改动, 请更新这里
"""


# noinspection PyProtectedMember
class CallerFinder:
    hierarchy = {
        'self'              : 3,
        'parent'            : 4,
        'grand_parent'      : 5,
        'great_grand_parent': 6
    }
    """
    hierarchy explaination:
        0 -> find_caller()
        1 -> base_print()
        2 -> log, loga, logd, logt, ...
        3 -> the direct caller which indirects to log/loga/logd/logt/...
        4 -> the caller of the direct caller
        5 -> the caller of caller of the direct caller
        6 -> ...
    """
    
    SELF_HIERARCHY = hierarchy['self']
    
    def interpret_hierarchy(self, h) -> int:
        if isinstance(h, int):
            return h
        else:
            return self.hierarchy.get(h, self.SELF_HIERARCHY)
    
    # ------------------------------------------------
    
    def find_caller_frame(self, hierarchy):
        hierarchy = self.interpret_hierarchy(hierarchy)
        return sys._getframe(hierarchy)
    
    @staticmethod
    def find_caller_by_frame(frame):
        """
        REFER:
            https://stackoverflow.com/questions/2203424/python-how-to-retrieve
            -class-information-from-a-frame-object
        
        ARGS:
            frame: e.g.
                last_frame = <frame at 0x0000021C15C8E9F8, file
                'D:/.../test.py', line 9, code <module>>
                    last_frame.f_code.co_filename -> 'D:/.../test.py'
                    last_frame.f_lineno -> 9
                    last_frame.f_code.co_name -> <module>
                        (you can see that in the source of last_frame.f_code)
        """
        filepath = frame.f_code.co_filename.replace('\\', '/')
        lineno = frame.f_lineno
        function = frame.f_code.co_name
        return filepath, lineno, function
    
    def find_caller_by_hierarchy(self, hierarchy):
        """
        find out who is the real caller.

        IN: hierarchy
        OT: (filepath, lineno, function, code_context)

        assumed here a callback chain:
            function `a()` called up function `b()`, function `b()` called up
            function `c()`, and function `c()` called up HERE (`find_caller()`).

            so the hierarchy would be:
                hierarchy = 0 -> stack()[0] -> reflected to function HERE
                hierarchy = 1 -> stack()[1] -> reflected to function `c()`
                hierarchy = 2 -> stack()[2] -> reflected to function `b()`
                hierarchy = 3 -> stack()[3] -> reflected to function `a()`
            so we can got any caller by the number of hierarchy from stack().

        an example of the stack() returns:
            stack()[1][0] -> the <frame> of caller (`c()`)
            stack()[1][1] -> the filepath where caller located
            stack()[1][2] -> the lineno where caller located
            stack()[1][3] -> the source code under that lineno

        NOTE: 目前 (2019年5月14日) 该函数只被用到过一次, 见 LKLogger.get_var_names().

        REFER:
            https://blog.csdn.net/qiqiyingse/article/details/70766993
            http://www.cnblogs.com/qq78292959/p/3289658.html
            https://www.cnblogs.com/yyds/p/6901864.html
        """
        hierarchy = self.interpret_hierarchy(hierarchy)
        
        context = stack()[hierarchy]
        
        filepath = context.filename.replace('\\', '/')
        lineno = context.lineno
        function = context.function
        if context.code_context:
            line = context.code_context[0].strip()
        else:
            line = ''
        
        return filepath, lineno, function, line


# ------------------------------------------------

class PathManager:
    launch_path = ''
    path_manager = None
    
    def __init__(self):
        # init path manager
        self.launch_path = abspath(sys.argv[0]).replace('\\', '/')
        
        self.path_manager = {self.launch_path: splitpath(self.launch_path)[1]}
        # -> {'d:/myprj/app/run.py': 'run.py'}
    
    def get_relpath(self, path):
        """
        IN: path: str. an absolute path.
        OT: (str) a relative path.
        """
        if not self.path_manager.get(path, ''):
            self.update_path_manager(path)
        return self.path_manager.get(path)
    
    def update_path_manager(self, new_abspath):
        """
        该函数用于将导入的模块所在的绝对路径加入到路径管理器中.

        :param new_abspath: str.
        :return:
        """
        new_relpath = calculate_relative_path(self.launch_path, new_abspath)
        # relpath -> relative path
        self.path_manager[new_abspath] = new_relpath


def calculate_relative_path(a, b):
    """
    已知两个绝对路径 a 和 b, 求 b 相对于 a 的相对路径.
    """
    a, b = a.split('/'), b.split('/')
    
    intersection = -1
    
    for m, n in zip(a, b):
        intersection += 1
        if m != n:
            break
    
    def backward():
        return (len(a) - intersection - 1) * '../'
    
    def forward():
        return '/'.join(b[intersection:])
    
    out = backward() + forward()
    return out


class MsgRecorder:
    
    def __init__(self):
        self.log_messages = []
        self.tag_messages = {'D': {}, 'I': {}, 'W': {}, 'E': {}, 'C': {}}
    
    def record(self, msg, tag=''):
        # print('[LKTEST]', 'lk_logger.py:180', msg, tag)
        
        self.log_messages.append(msg)
        if tag:
            node = self.tag_messages.setdefault(tag[0], {})
            node = node.setdefault(tag, [])
            node.append(msg)
    
    def show_important_messages(self, show_details=True, output='console'):
        if not self.tag_messages:
            return
        
        # collect messages
        temp_msg_container = []
        
        # details info
        if show_details:
            for msg_chunk in self.tag_messages.values():  # type: dict
                """
                'D' -> msg_chunk = {
                    'D2324': ['hello', 'nihao', ...],
                    'D3225': [...],
                    'D...': ...
                }
                """
                for k, v in msg_chunk.items():
                    if k.startswith('[TEMPRINT'):  # TODO
                        continue
                    temp_msg_container.extend(sorted(v))
        
        # summary info
        for msg_chunk in self.tag_messages.values():  # type: dict
            for k, v in msg_chunk.items():
                temp_msg_container.append(
                    f'\t\t{k}: {len(v)}\t>>\t{v[0] if v else ""}'
                )
        
        """
        NOTE: 注意前后顺序. temp_msg_container 需要先装载 details info, 后装载
        summary info. 这样有利于阅读.
        """
        
        # print the msg or save it into file.
        if output == 'console':
            for i in temp_msg_container:
                print(i)
        else:
            with open(output, 'w') as file:
                file.write('\n'.join(temp_msg_container))
        
        # also take record to log_messages. (for the future to do dump_log())
        self.log_messages += temp_msg_container
    
    def dump_log(self, output, launch_path):
        curtime = time()
        timestamp = generate_timestamp('_ymd_hns', curtime)
        
        if '.txt' in output:
            # 说明 output 是一个文件路径.
            output = output.replace(
                '.txt', '{}.txt'.format(timestamp)
            )
        else:
            # 说明 output 是一个目录路径, 比如说是 '../log/'
            assert launch_path, 'if you define the output to be a dir, you ' \
                                'need to give me the launcher\' filepath.'
            filename = splitpath(launch_path)[1].replace(
                '.py', '{}.txt'.format(timestamp)
            )
            """
            当 output 是一个目录时, 则默认使用启动文件的文件名作为生成的日志的文件名.
            启动文件由 LKLogger.launch_path 提供.
            注意 LKLogger.launch_path 提供的是绝对路径.
            """
            output = output.strip('/') + '/' + filename
        
        with open(output, encoding='utf-8', mode='w') as f:
            prefix = f"""
script launched at {launch_path}.
script filename is {splitpath(launch_path)[1]}.
log dumped at {generate_timestamp('y-m-d h:n:s', curtime)}.

----------------------------------------------------------------

            """
            f.write(prefix.strip(' '))
            f.write('\n'.join(self.log_messages))
        
        return output


# ------------------------------------------------

class AstAnalyser:
    
    def __init__(self):
        # see self.fake_text()
        self.char = re.compile(r'\w')
        # `f'{A}'` -> ``
        self.string_fmt = re.compile(r'^[frb]*["\']')
        # `A(` -> `A`
        self.strip_start = re.compile(
            r'\(.*$'
        )
        # `A  # B` -> `A`
        self.strip_end = re.compile(
            r'(?<=,) ?[a-zA-Z]+=.+$'
            r'|\) *#.*$'
            r'|\) *$'
        )
    
    def fake_text(self, text: str):
        """
        一个有意思的现象, 当 text 中含有汉字等非西文字符时, 会导致 ast 在解析时的
        col_offset 计算错误. 该问题在 https://bugs.python.org/issue21295 中有所体现,
        并得到了一些解释:
            ...col_offset 是生成节点的第一个 token 的 utf-8 字节偏移.
        由于一个汉字占用两个字节, 就产生了 col_offset 偏移的问题.
        为了解决它, 我们需要将汉字转换成一个伪造的字母表示. 例如:
            `lk.loga('你好')` -> `lk.loga('xx')`
        """
        return re.sub(self.char, 'x', text)
    
    def main(self, text: str):
        """
        IN: text: make sure it had been stripped.
        OT: list/None.
        """
        out = []
        
        last_index = 0
        
        try:
            fake_text = self.fake_text(text)
            # print('[LKTEST]', 'lk_logger.py:320', fake_text)
            root = ast_parse(fake_text)
        except SyntaxError:
            """
            这种情况发生的原因是, text 是不符合语法的代码. 例如:
                ```
                lk.logt(A, B
                ```
                B 的右侧没有括号封尾, 因此不符合语法规范. 将导致此项报错.
            遇到这种错误, 会返回 None. 请调用方判断并认定为不可解析.
            """
            return None
        
        for a in iter_child_nodes(root):  # _ast.Expr
            for b in iter_child_nodes(a):  # _ast.Call
                for c in iter_child_nodes(b):  # _ast.Attribute, ...
                    if getattr(c, 'col_offset', 0) == 0:
                        continue
                    else:
                        curr_index = c.col_offset
                    # print(
                    #     '[LKTEST]', 'lk_logger.py:330', curr_index, type(c),
                    #     getattr(c, 'id', None)
                    # )
                    r = text[last_index:curr_index]
                    out.append(self.sanitize_string(r))
                    last_index = curr_index
                break
            break
        out.append(text[last_index:])
        
        out[0] = self.sanitize_string(out[0], loc='start')
        out[-1] = self.sanitize_string(out[-1], loc='end')
        
        # print('[LKTEST]', 'lk_logger.py:360', out)
        # text = `lk.loga("ABC", a)` -> out = ['lk.loga', '', 'a']
        
        return out[1:]  # -> ['', 'a']
    
    def sanitize_string(self, s: str, loc=None):
        """
        IN: s
            loc: None/'start'/'end'. location. 元素在列表中的位置.
        OT:
        """
        if loc == 'start':
            if s.endswith('('):
                s = s[:-1]
                # 'lk.loga(' -> 'lk.loga'
            else:
                s = re.sub(self.strip_start, '', s)
                # 'lk.loga( ' -> 'lk.loga'
        if loc == 'end':
            s = re.sub(self.strip_end, '', s)
            # 1) 'a)  # this is a comment' -> 'a'
            # 2) 'a, h="parent")' -> 'a'
        
        # common strip
        s = s.strip(', ')
        
        if self.string_fmt.findall(s):
            return ''
        else:
            return s


# ------------------------------------------------

class LKLogger:
    """
    注: 本类中的所有 h = 'self' 均指向 log 函数的直接调用者 (direct caller). 'parent'
    均指向直接调用者的调用者, 'grand_parent' 是直接调用者的调用者的调用者, 以此类推.
        例如, 外部函数 fx() 调用了 LKLogger.log(), 则 fx() 是直接调用者.
        例如, 外部函数 fx() 调用了 LKLogger.over(), 而 over() 调用了 LKLogger.log(), 
        则 over() 是直接调用者, fx() 是间接调用者. (因此你可以看到, 为了让指向到达外部函数 
        fx(), over() 函数中特意将层级参数上调为 'parent' 了)
    """
    log_enable = True
    
    start_time = 0
    end_time = 0
    
    lite_mode = False  # TODO: more works need to be done.
    
    def __init__(self):
        self.finder = CallerFinder()
        self.recorder = MsgRecorder()
        self.ast_analyser = AstAnalyser()
        self.path_manager = PathManager()
        
        self.code_tracker = {}
        """
        -> {`(str)filepath`: {`(int)lineno`: `(list)var_names`}, ...}
        """
        
        # FIXME WARNING: not ready to use.
        self.log_style = {  # related to self.set_log_style
            'show_func'          : True,
            'graphic_progressbar': False,
            'align_counter'      : True,
        }
        
        # start timing.
        self.start_time = time()
        print('start time = {}'.format(
            generate_timestamp('y-m-d h:n:s', self.start_time))
        )
        self.recorder.record(self.path_manager.launch_path)
    
    def set_log_style(self, style: dict):
        """
        overwrite self.log_style configurations.
        
        support properties:
            `show_func`: bool. default True.
                True: e.g. printing 'myapp.py:12 >> main() >> hello'
                False: e.g. printing 'myapp.py:12 >> hello'
            `graphic_progressbar`: bool. default False.
                True: e.g. '■■■■-------------------------- 13%' (writing and 
                swiping msg in one line.)
                False: e.g.
                    [01/30] loop index count 1
                    [02/30] loop index count 2
                    [03/30] loop index count 3
                    ...
            `align_counter`: bool. default True.
                True: e.g. '[01/30] loop index count 1'
                False: e.g. '[1/30] loop index count 1'
            
        e.g. style = {'shor_func': False, 'align_counter': False}
        """
        self.log_style.update(style)
    
    # ------------------------------------------------
    
    def base_print(self, *msg, caller='log', h='self', **kwargs):
        """
        
        """
        # print('[LKTEST]', 'lk_logger.py:340', msg)
        
        if self.log_enable is False:
            return
        
        # personal settings (aka log style)
        is_count_up = bool(caller.endswith('x'))  # e.g. 'logx', 'logax', ...
        count = self.count_up(is_count_up)
        tag = kwargs.get('tag', '')
        divide_line = kwargs.get('divide_line', '')
        prtend = ' ' if (count or tag or divide_line) else ''
        
        if self.lite_mode:
            # prefix
            prefix = '{}{}{}{}'.format(
                count, divide_line, tag, prtend
            )
        else:
            frame = self.finder.find_caller_frame(h)
            filepath, lineno, function = self.finder.find_caller_by_frame(frame)
            filepath = self.path_manager.get_relpath(filepath)
            if function != '<module>':
                function += '()'
            
            # prefix
            prefix = '{}:{}\t>>\t{}\t>>\t{}{}{}{}'.format(
                filepath, lineno, function, count, divide_line, tag, prtend
            )
        
        print(prefix, end='')
        """
        注意这里我们把 print 的 end 参数设为空字符串, 而由 prtend 控制是否在末尾加空格.
        这样做的目的是, 在 MsgRecorder 记录的时候, 也能记录到这个 prtend; 否则就会在 dump
        的时候发现对齐不是很美观 (特别是涉及到 log*x, logd, logt, logdt 的对齐的时候).
        """
        
        # print mainbody
        # msg = (i.replace('\r', '') for i in msg)  # 去除 \\r 的影响
        # 注: 去除 \\r 的方法暂时不用. 因为它会引起 self.recorder.record() 记录失败的问
        # 题. 原因尚在调查中.
        print(*msg, sep=';\t')
        
        # take records
        msg = map(str, msg)
        self.recorder.record(prefix + ';\t'.join(msg), tag=tag)
    
    # ------------------------------------------------
    
    def log(self, *data, h='self'):
        """
        log (normal style).
        """
        self.base_print(*data, caller='log', h=h)
    
    def loga(self, *data, h='self'):
        """
        log in advanced mode.
        
        NOTICE: 暂时 (2019年7月7日) 无法解决以下问题:
            def foo(*x):
                lk.loga(*x)
        
            
            foo(1, 2, 3)
        在这种情况下, 只能打印出第一个参数的值: *x = 1
        """
        # print('[LKTEST]', 'lk_logger.py:420', id(data), data)
        
        var_names = self.get_var_names('loga', h)
        if var_names is not None:
            data = [f'{i} = {j}' if i else f'{j}'
                    for i, j in zip(var_names, data)]
        
        self.base_print(*data, caller='loga', h=h)
    
    def logd(self, *data, style='-', length=64, h='self'):
        """
        log with divide line.
        """
        var_names = self.get_var_names('logd', h)
        if var_names is not None:
            data = [f'{i} = {j}' if i else f'{j}'
                    for i, j in zip(var_names, data)]
            
        divide_line = style * length
        self.base_print(*data, caller='logd', h=h,
                        divide_line=divide_line)
    
    def logt(self, tag, *data, h='self'):
        """
        log with tag.

        ARGS:
            tag: support list:
                D, I, W, E, C
                DEBUG, INFO, WARNING, ERROR, CRITICAL
                D0323, I3234, W3145, E2345, C3634, ... (use live templates to
                generate a timestamp (like `MMSS`) as a uniq code stamp.)
            data
            h
        """
        var_names = self.get_var_names('logt', h)
        if var_names is not None:
            data = [f'{i} = {j}' if i else f'{j}'
                    for i, j in zip(var_names, data)]
        
        self.base_print(*data, caller='logt', h=h, tag=tag)
    
    # ------------------------------------------------
    
    def logx(self, *data, h='self'):
        """
        log with index counter.
        """
        self.base_print(*data, caller='logx', h=h)
        # count_up=True
        # 这个设不设置无所谓, 因为 base_print() 是不会看的, 一律当做 True 处理.
    
    def logax(self, *data, h='self'):
        """
        log in advanced with index counter.
        """
        var_names = self.get_var_names('logax', h)
        if var_names is not None:
            data = [f'{i} = {j}' if i else f'{j}'
                    for i, j in zip(var_names, data)]
        self.base_print(*data, caller='logax', h=h)
    
    def logdx(self, *data, style='-', length=64, h='self'):
        """
        log with divide line and index counter.
        """
        var_names = self.get_var_names('logdx', h)
        if var_names is not None:
            data = [f'{i} = {j}' if i else f'{j}'
                    for i, j in zip(var_names, data)]
        divide_line = style * length
        self.base_print(*data, caller='logdx', h=h,
                        divide_line=divide_line)
    
    def logtx(self, tag, *data, h='self'):
        """
        log with tag and index counter.
        """
        var_names = self.get_var_names('logtx', h)
        if var_names is not None:
            data = [f'{i} = {j}' if i else f'{j}'
                    for i, j in zip(var_names, data)]
        
        self.base_print(*data, caller='logtx', h=h, tag=tag)
    
    # ------------------------------------------------
    
    def logdt(self, tag, *data, style='-', length=64, h='self'):
        """
        log with divide line and index counter.
        """
        var_names = self.get_var_names('logdt', h)
        if var_names is not None:
            data = [f'{i} = {j}' if i else f'{j}'
                    for i, j in zip(var_names, data)]
        divide_line = style * length
        self.base_print(*data, caller='logdt', h=h, tag=tag,
                        divide_line=divide_line)
    
    def logdtx(self, tag, *data, style='-', length=64, h='self'):
        var_names = self.get_var_names('logdtx', h)
        if var_names is not None:
            data = [f'{i} = {j}' if i else f'{j}'
                    for i, j in zip(var_names, data)]
        divide_line = style * length
        self.base_print(*data, caller='logdtx', h=h, tag=tag,
                        divide_line=divide_line)
    
    # ------------------------------------------------
    
    def wrap_counter(self, x):
        d = int(x) if isinstance(x, (float, int)) else len(x)
        self.counter_denominator = d
        self.counter = 0
        return x
    
    def over(self, total_count=-1):
        if total_count == -1:
            total_count = max(self.total_count, self.counter_denominator)
        
        h = 'parent'
        
        self.logd('计时结束', h=h)
        self.end_time = time()
        
        self.log('开始运行: {}'.format(
            generate_timestamp('y-m-d h:n:s', self.start_time)
        ), h=h)
        self.log('结束运行: {}'.format(
            generate_timestamp('y-m-d h:n:s', self.end_time)
        ), h=h)
        
        # calculate duration
        total_elapsed_time_sec = self.end_time - self.start_time
        if total_elapsed_time_sec < 0.01:
            duration = '{}ms'.format(
                round(total_elapsed_time_sec * 1000, 2))
        elif total_elapsed_time_sec < 60:
            duration = '{}s'.format(round(total_elapsed_time_sec, 2))
        else:
            duration = '{}min'.format(round(total_elapsed_time_sec / 60, 2))
        self.log('总耗时 {}'.format(duration), h=h)
        
        # calculate speed
        if total_count > 0:
            speed = total_elapsed_time_sec / total_count
            if speed < 0.01:
                speed *= 1000
                unit = 'ms'
            else:
                unit = 's'
            self.log(
                '共处理 {} 个. 平均速度 {}{}/个'.format(
                    total_count, round(speed, 2), unit
                ), h=h)
    
    # ------------------------------------------------
    
    def print_important_msg(self, show_details=True, output='console'):
        if not self.recorder.tag_messages:
            return
        self.logd('here collected important messages', h='parent')
        self.recorder.show_important_messages(show_details, output)
    
    def dump_log(self, output=''):
        """
        PARAM:
            output: str. 可以传入一个 log 目录, 或者指定一个具体的 log 文件作为输出目标.
        """
        if output == '':
            from .file_sniffer import getpath
            output = relpath(getpath('log/')).replace('\\', '/')
        logpath = self.recorder.dump_log(output, self.path_manager.launch_path)
        self.log(f'log dumped at "{logpath}"', h='parent')
    
    # ------------------------------------------------ loga helpers
    
    def get_var_names(self, caller, h='self'):
        frame = self.finder.find_caller_frame(h)
        filepath, lineno, function = self.finder.find_caller_by_frame(frame)
        # print('[LKTEST]', 'lk_logger.py:590', filepath, lineno, function)
        
        try:
            return self.code_tracker[filepath][lineno]
        except KeyError:
            # NOTE: this method will slow down the program, so please use it as
            # less as you can.
            filepath_, lineno_, function_, line = \
                self.finder.find_caller_by_hierarchy('self')
            """
            注: 以下称 'self' 级别的 caller 为 direct caller, >= 'self' 级别的
            caller 为 indirect caller.
            
            注意点1:
                这里传的层级必须是 'self', 因为这里我们想要拿到的是 direct caller 的
                line.
            
            注意点2:
                self.finder.find_caller_by_hierarchy 返回的 filepath_, lineno_ 都
                不使用, 而使用本函数开头从 self.finder.find_caller_by_frame() 获得的
                filepath 和 lineno.
                从原理上来看, filepath, lineno 代表的是 direct caller 所在的文件名和代
                码行号, 而 filepath_, lineno_ 代表的是 indirect caller 的位置.
                如果我们使用 indirect caller 的位置, 则会造成下次在已知 direct caller
                的前提下, 还要重复一遍 KeyError 的流程, 就造成了效率低下.
                因此我们不用 indirect caller 的 filepath_, lineno_, 而使用 direct 
                caller 的 filepath, lineno 来存储 indirect caller 的上下文信息.
                注: 这里只是针对于 self.code_tracker 的策略, 不影响 self.base_print() 
                的正常执行, 也不会影响最终输出的效果. 可以放心使用.
            """
            
            var_names = self.split_vars_from_source_code_line(line)
            # print('[LKTEST]', 'lk_logger.py:620', line, var_names)
            
            if var_names is not None:
                if caller in ('logt', 'logtx', 'logdt', 'logdtx'):
                    """
                    这些 caller 的原型都是 logt.
                    logt 有个特殊的地方在于, 它的第一个参数是 tag. 我们必须把它剔除.
                    """
                    var_names.pop(0)
            
            node = self.code_tracker.setdefault(filepath, {})
            node[lineno] = var_names
            
            return var_names
    
    def split_vars_from_source_code_line(self, raw_line):
        """
        extract the core, intuitive content from the raw source code line.

        IO: 'lk.log(A, "B", C[D])' -> ['A', '', 'C[D]']

        NOTE: this method will slow down the program, so please use it as less
        as possible.
        """
        if not raw_line.startswith('lk.log'):
            '''
            注: 暂不支持智能处理折行的情况:
                lk.loga(
                    a, b
                )
                lk.loga(a,
                        b)
            原因在于, 对于折行情况, stack caller 只能追踪到最后一行的源码内容.
            因此, 针对这类情况, 本函数将只返回 raw_data 的处理结果.
            '''
            return None
        else:
            return self.ast_analyser.main(raw_line)
    
    # ------------------------------------------------ 
    
    total_count = 0
    counter_denominator = 0
    counter = 0
    
    def count_up(self, is_count_up):
        if not is_count_up:
            return ''
        
        # NOTICE: not support to make out differnt loops for now.
        self.counter += 1
        count = str(self.counter)
        
        if self.counter_denominator > 0:
            length = len(str(self.counter_denominator))
            tag = '[{}/{}]'.format(
                count.zfill(length), self.counter_denominator
            )
        else:
            tag = f'[{count}]'
        
        return tag
    
    # ------------------------------------------------ backward compatibility
    
    reg = re.compile(r'^\[[DIWEC]\d*\]')
    
    # made for backward compatibility. this is used to find old tags.
    
    def prt(self, data, count_up=False, hierarchy=''):
        if hierarchy == '':
            hierarchy = 'parent'
        else:
            """
            以前的默认值是2, 现在的默认值是4, 所以要加二.
            """
            hierarchy += 2
        
        tag = self.reg.findall(data)
        if tag:
            tag = tag[0]
            data = data.replace(tag, '', 1)
            
            if count_up:
                self.logtx(tag, data, h=hierarchy)
            else:
                self.logt(tag, data, h=hierarchy)
        else:
            if count_up:
                self.logax(data, h=hierarchy)
            else:
                self.loga(data, h=hierarchy)
    
    def smart_prt(self, *data, count_up=False, hierarchy=''):
        if hierarchy == '':
            hierarchy = 'parent'
        else:
            """
            以前的默认值是3, 现在的默认值是4, 所以要加一.
            """
            hierarchy += 1
        
        if isinstance(data[0], str) and self.reg.findall(data[0]):
            tag = self.reg.findall(data[0])[0]
            data = list(data)
            data[0] = data[0].replace(tag, '', 1)
            
            if count_up:
                self.logtx(tag, *data, h=hierarchy)
            else:
                self.logt(tag, *data, h=hierarchy)
        else:
            if count_up:
                self.logax(*data, h=hierarchy)
            else:
                self.loga(*data, h=hierarchy)
    
    def divider_line(self, data='', count_up=False, style='-', length=64,
                     mirror=False, hierarchy=''):
        if hierarchy == '':
            hierarchy = 'parent'
        else:
            """
            以前的默认值是3, 现在的默认值是4, 所以要加一.
            """
            hierarchy += 1
        
        if mirror:
            data += style * length
        
        if count_up:
            self.logdx(data, style=style, length=length, h=hierarchy)
        else:
            self.logd(data, style=style, length=length, h=hierarchy)
    
    def init_counter(self, x=0):
        self.counter_denominator = x
        self.counter = 0


# ------------------------------------------------

lk = LKLogger()


# ------------------------------------------------

def testflight():
    a = 'aaa'
    b = 'bbb'
    
    # 普通
    # lk.loga(a)
    
    # 有注释干扰
    # lk.loga(a)  # this is a comment.
    
    # 有字符串参数
    # lk.loga('a string', a)
    
    # 复杂字符串
    # lk.loga('"A" to "B", {}'.format(a), a)
    
    # 复合 (调用)
    # lk.loga(type(b), a.replace('a', 'b'))
    
    # 复合 (表达式)
    # lk.loga(a if a else None)
    
    # 复合 (切片)
    pass
    
    # 特殊 (换行)
    pass
    
    # 不规则
    # lk.loga( 'A', a )
    
    # kw 参数
    # lk.loga(a, h='parent')
    
    # logt 打印
    # lk.logt('[D0535]', 'hi', a)
    
    # 折行 1
    lk.loga(
        a,
        b
    )
    
    # 折行 2
    lk.loga(a,
            b)
    
    # 折行 3
    lk.loga(a, '------'
               '++++++', b)


if __name__ == '__main__':
    testflight()
