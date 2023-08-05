from os import path as ospath

import xlsxwriter

from .lk_logger import lk


class ExcelWriter:
    """
    ExcelWriter 是对 xlsxwriter 模块的封装实现. 旨在提供更加灵活, 便捷的表格写入工作.
    
    xlsxwriter 相比于 xlwt 具有以下优点:
        - 同样设置 10 号字, xlsxwriter 传入数字 10, xlwt 传入的是 200 (1:20 的换算关系),
          前者更人性化
        - xlsxwriter 有写入行/列的方法, xlwt 只有单个单元格的写入方法
        - xlsxwriter 支持自动识别字符串类型的数字并转换为 int 的选项
        - xlsxwriter 在写入大数据时, 支持 constant memory 模式 (针对内存的优化模式)
        - xlsxwriter 输出 xlsx 格式的表格, xlwt 则为 xls 格式
        - 由于 xls 格式的限制, 每个 sheet 行/列最多允许 65535 个单元格, 这导致
          ExcelWriterR 不得不用大量的 side methods 来优化输出体验
        - 由于 xls 格式的限制, 当单个单元格要写入的字符串长度大于 35000 时, 会导致报错
        - xls 输出的文件体积比 xlsx 大
        - 当覆写单元格时, xlwt 会报错
        - ExcelWriter 相比 ExcelWriterR 结构更加简明, 且在功能体验上更好
        - ExcelWriterR 默认不支持全局风格设置, 需要通过 WorkbookYahei 和
          WorksheetYahei 来实现
        - xlwt 设置样式操作比 xlsxwriter 繁琐
    
    REF:
        https://www.jianshu.com/p/187e6b86e1d9
    """
    
    # 路径初始化
    filepath = ''
    # excel 初始化
    book, sheet = None, None
    # 游标初始化
    sheetx, rowx = 0, -1
    
    def __init__(self, filepath: str, sheetname='', constant_memory=False):
        """
        ARGS:
            filepath
            sheetname: 当为空时, 将使用默认的 sheet 命名方式 ('sheet 1'), 或者您也可以定
                义为自己想要的命名. 特别的, 您可以传入 None, 这是一个特殊的标志, 用来表示
                "不在 __init__() 阶段创建 sheet".
            constant_memory: 当写入数据非常大时, 开启此选项.
        """
        if filepath.endswith('.xls'):
            filepath += 'x'
            lk.logt('[I2504]', 'ExcelWriter 不支持 xls 格式的输出, 将自动转为 xlsx',
                    filepath, h='parent')
        self.filepath = filepath
        
        # ------------------------------------------------ excel 配置
        
        # 创建 workbook
        self.book = xlsxwriter.Workbook(
            filename=filepath,
            options={
                'strings_to_numbers'       : True,  # 自动转换字符串类型的数字
                'strings_to_urls'          : False,  # 自动转换链接为蓝色下划线链接
                'constant_memory'          : constant_memory,
                'default_format_properties': {
                    'font_name': '微软雅黑',  # 字体 (默认 "Arial")
                    'font_size': 10,  # 字体字号 (默认是 11 号字)
                    # 'bold': False,  # 字体加粗
                    # 'border': 1,  # 单元格边框宽度
                    # 'fg_color': '#F4B084',  # 单元格背景色
                    # 'align': 'left',  # 单元格水平对齐方式
                    # 'valign': 'vcenter',  # 单元格垂直对齐方式
                    # 'text_wrap': False,  # 自动换行 (默认为 False)
                },
            }
        )
        
        # 配置合并单元格时的格式
        self.merge_format = self.book.add_format({
            # 'font_name': '微软雅黑',  # 字体 (默认 "Arial")
            # 'font_size': 10,  # 字体字号 (默认是 11 号字)
            # 'bold': False,  # 字体加粗
            # 'border': 1,  # 单元格边框宽度
            # 'fg_color': '#F4B084',  # 单元格背景色
            'align' : 'center',  # 单元格水平对齐方式
            'valign': 'vcenter',  # 单元格垂直对齐方式
            # 'text_wrap': False,  # 自动换行 (默认为 False)
        })  # REF: https://blog.csdn.net/lockey23/article/details/81004249
        
        # 创建 sheet
        if sheetname is not None:
            self.add_new_sheet(sheetname)
    
    # ----------------------------------------------------------------
    
    def write(self, rowx, colx, data):
        """
        写入一个单元格.
        ARGS:
            rowx: int. 行号, 从 0 开始数.
            colx: int. 列号, 从 0 开始数.
            data: str/bool/int/float/None. 单元格内容, 接受 python 基本数据类型.
        """
        self.sheet.write(rowx, colx, data)
    
    def writeln(self, *row, auto_index=False, clean_values=False):
        """
        顺序性地写入一行数据.
        """
        if clean_values:
            row = self.clean_values(row)
        index = self._increase_rowx()
        if self.rowx == 0 or not auto_index:
            self.sheet.write_row(self.rowx, 0, row)
        else:
            self.sheet.write(self.rowx, 0, index)
            self.sheet.write_row(self.rowx, 1, row)
    
    def writerow(self, rowx, *row, offset=0, clean_values=False):
        """
        在指定行写入一行数据. 允许指定起始格 (offset=0).
        """
        if clean_values:
            row = self.clean_values(row)
        self.sheet.write_row(rowx, offset, row)
    
    def writecol(self, colx, *row, offset=1, clean_values=False):
        """
        在指定列写入一列数据. 允许指定起始格 (offset=1).
        """
        if clean_values:
            row = self.clean_values(row)
        self.sheet.write_column(offset, colx, row)
    
    def write_merging_cells(self, *rows):
        """
        符号: '-' 表示向左合并, '~' 表示向上合并.
        
        IN: (
                [A, B, C, -, D],
                [~, ~, E, F, ~]
            )
        OT: | A | B | C   * | D |
            | * | * | E | F | * |
            
        NOTE: 如果需要画一个矩形, 建议优先使用 '-'. 例如:
            (
                [A, B, -, C],
                [D, ~, -, E],  # 注意第二行第三个, 建议使用 '-', 处理速度更快一点
            )
            | A | B  * | C |
            | D | *  * | E |
        """
        length = tuple(len(x) for x in rows)
        assert min(length) == max(length)
        
        # encoding mask
        rows_mask = []
        uid_2_cell = {}  # {uid: cell}
        uid = 0  # generate uid simply by adding one by one...
        
        for rowx, row in enumerate(rows):
            node = []
            for colx, cell in enumerate(row):
                if cell == '-':
                    node.append(node[-1])
                elif cell == '~':
                    node.append(rows_mask[rowx - 1][colx])
                else:
                    uid += 1
                    node.append(uid)
                    uid_2_cell[uid] = cell
            rows_mask.append(node)
            
        merging = {}  # {uid: [(rowx, colx), ...]}
        
        for rowx, row in enumerate(rows_mask):
            for colx, uid in enumerate(row):
                node = merging.setdefault(uid, [])
                node.append((rowx, colx))
        
        for uid, positions in merging.items():
            cell = uid_2_cell[uid]
            if len(positions) == 1:
                self.write(*positions[0], cell)
            else:
                self.merge_cells(*positions[0], *positions[-1], cell)
    
    def merge_cells(self, x1, y1, x2, y2, data):
        self.sheet.merge_range(x1, y1, x2, y2, data, self.merge_format)
    
    # ------------------------------------------------

    @staticmethod
    def clean_values(row):
        """
        caller: writeln, writerow, writecol
        注: 本方法在 caller 中默认是不启用的.
        """
        return tuple(
            v.strip() if isinstance(v, str) else v for v in row
        )

    # ------------------------------------------------
    
    def _increase_rowx(self):
        """
        自动增长序号.
        """
        self.rowx += 1
        return self.rowx
    
    def add_new_sheet(self, sheet_name='', prompt=False):
        self.sheetx += 1
        self.rowx = -1
        
        # create sheet name
        if not sheet_name:
            sheet_name = f'sheet {self.sheetx}'  # -> 'sheet 1', 'sheet 2', ...
        if prompt:
            lk.logt('[D1344]',
                    f'add new sheet: "{sheet_name}" (sheetx {self.sheetx})',
                    ospath.split(self.filepath)[1])
        
        self.sheet = self.book.add_worksheet(sheet_name)
    
    # ------------------------------------------------
    
    def save(self):
        lk.logt('[I1139]', f'excel saved to "{self.filepath}"', h='parent')
        self.book.close()
