"""
excel_writer 1.6.0
"""
from os import path as ospath

from xlwt import *
from xlwt import Utils
from xlwt.compat import unicode_type

from .lk_logger import lk


class ExcelWriter:
    """
    ExcelWriter 是对 xlwt 模块的封装实现. 旨在提供更加灵活, 便捷的表格写入工作.
    NOTE (2019-09-10): this class is depreciated to use. please use ExcelWriter
    instead.
    """
    
    # 路径初始化
    filepath = ''
    
    # 自动化配置初始化
    automation = None
    
    # excel 初始化
    book, sheet, header = None, None, None
    
    # 游标初始化
    # 注: bookx, sheetx 使用的是从 1 开始数的, rowx 是从 0 开始数的. 原因在于, bookx,
    # sheetx 将被用于对外输出时给用户看, 而 rowx 用于在内部控制序列的增长逻辑.
    bookx, sheetx, rowx, rowx_offset = 1, 0, -1, 0
    
    # 容量设计
    # 每张表最多有 5 个 sheet, 每个 sheet 最多有 50000 行数据. 每张表最多 25w 条数据. 当写
    # 入量超出容量设计时, 将自动创建新的 sheet/book 来盛装.
    rowx_limit, sheetx_limit = 50000, 5
    
    def __init__(self, filepath: str):
        if filepath.endswith('.xlsx'):
            lk.logt('[W2402]', 'ExcelWriter 不支持 xlsx 格式输出, 将自动转为 xls',
                    h='parent')
            filepath = filepath[:-1]
        
        # 路径配置
        self.filepath = filepath
        
        # excel 配置
        self.book = WorkbookYahei()
        self.add_new_sheet()
        
        # 自动化配置
        self.automation = {
            'auto_create_header_in_new_sheet'                   : True,
            'consistent_growing_rowx_when_auto_create_new_sheet': True
        }
    
    def set_auto_header(self, state: bool):
        """
        是否允许自动创建新 sheet 的同时创建标题头.
        注: 该自动化仅作用于 ExcelWriter 在容量溢出时的内部反应, 当人为地创建新 sheet 时,
        不会触发该机制.
        """
        self.automation['auto_create_header_in_new_sheet'] = state
    
    def set_consistent_growing_rowx(self, state: bool):
        """
        是否在新 sheet 中沿用上次的 index 结尾计数并继续.
        state:
            True: 假设单 sheet 的容量上限为 5w 行, 则后续 sheet 的 index 分别从 50001,
                100001, 150001, ... 开始. (默认)
            False: 假设单 sheet 的容量上限为 5w 行, 则后续 sheet 的 index 均从 1 开始.
        """
        self.automation[
            'consistent_growing_rowx_when_auto_create_new_sheet'
        ] = state
    
    # ----------------------------------------------------------------
    
    def write(self, rowx, colx, data):
        """
        写入一个单元格.
        注: 不要重复写入同一个单元格, 否则会报错.

        ARGS:
            rowx: int. 行号, 从 0 开始数.
            colx: int. 列号, 从 0 开始数.
            data: str/bool/int/float/None. 单元格内容, 接受 python 基本数据类型.
        """
        self.sheet.write(rowx, colx, data)
    
    def writeln(self, *row, auto_index=False, offset=0):
        """
        (顺序性地) 写入一行数据.
        注: 如果您需要在指定的行写入, 请使用 self.write_row_values() 方法.
        """
        index = self._increase_rowx()
        if index == -1:
            # repairing
            if self.automation[
                'consistent_growing_rowx_when_auto_create_new_sheet'
            ]:
                self.rowx_offset += self.rowx_limit
            
            self.add_new_sheet()  # reset self.rowx = -1
            
            self._increase_rowx()  # -> 0, 50000, 100000, ...
            if self.automation['auto_create_header_in_new_sheet']:
                self.write_row_values(self.sheet, 0, *self.header)
            index = self._increase_rowx()  # -> 1, 50001, 100001, ...
        
        if self.rowx == 0 \
                and self.automation['auto_create_header_in_new_sheet']:
            self.header = row
            auto_index = False
        
        if auto_index:
            self.write_row_values(self.rowx, index, *row, offset=offset)
        else:
            self.write_row_values(self.rowx, *row, offset=offset)
    
    def write_row_values(self, rowx, *data, offset=0):
        for colx, data in enumerate(data, offset):
            if isinstance(data, str) and len(data) > 32000:
                # Exception: String longer than 32767 characters
                lk.logt('[ExcelWriter][W1717]',
                        'string longer than 32000 characters, it will be '
                        'substituted with [◆WARNING:DATADAMAGED◆]',
                        rowx, h='grand_parent')
                data = '[◆WARNING:DATADAMAGED◆]' + data[0:1000]
            self.sheet.write(rowx, colx, data)
    
    def write_col_values(self, colx, *data, offset=0):
        for rowx, data in enumerate(data, offset):
            if isinstance(data, str) and len(data) > 32000:
                # Exception: String longer than 32767 characters
                lk.logt('[ExcelWriter][W1718]',
                        'string longer than 32000 characters, it will be '
                        'substituted with [◆WARNING:DATADAMAGED◆]',
                        rowx, h='grand_parent')
                data = '[◆WARNING:DATADAMAGED◆]' + data[0:1000]
            self.sheet.write(rowx, colx, data)
    
    # ----------------------------------------------------------------
    
    def _increase_rowx(self):
        """
        自动增长 rowx (行序号), 并具有判断容量是否溢出的功能.
        """
        self.rowx += 1
        if self.rowx <= self.rowx_limit:
            return self.rowx_offset + self.rowx
        else:
            return -1
    
    def _increase_sheetx(self):
        """
        自动增长 sheetx (分页数), 并具有处理容量溢出的功能.
        """
        self.sheetx += 1  # out: 1, 2, 3, ...
        
        if self.sheetx > self.sheetx_limit:
            self.add_new_book()  # reset sheetx = 0, rowx = -1
            self.sheetx = 1
    
    def _increase_bookx(self):
        """
        自动增长 bookx (分表文件数), 由于无容量上限, 所以不具备容量溢出的判断.
        """
        self.bookx += 1
    
    def add_new_sheet(self, sheet_name=''):
        # set sheetx +=1 , reset rowx = -1
        self._increase_sheetx()
        self.rowx = -1
        
        if not sheet_name:
            sheet_name = f'sheet {self.sheetx}'  # -> 'sheet 1', 'sheet 2', ...
        if self.sheetx > 1:
            lk.logt('[ExcelWriter][D1344]',
                    f'add new sheet: "{sheet_name}" (sheetx {self.sheetx})',
                    ospath.split(self.filepath)[1])
        
        self.sheet = self.book.add_sheet(sheet_name)
    
    def add_new_book(self):
        # 获取文件名后缀: https://www.cnblogs.com/hixiaowei/p/8438930.html
        self.book.save(self._get_subbook_name())
        
        # set bookx += 1, reset sheetx = 0, rowx = -1
        self._increase_bookx()
        self.sheetx = 0
        self.rowx = -1
        
        lk.logt('[ExcelWriter][I1540]',
                f'add new book: "{self._get_subbook_name()}" '
                f'(bookx {self.bookx})')
        
        self.book = WorkbookYahei()
    
    def _get_subbook_name(self, is_final=False):
        """
        :param is_final: bool
            True: 表示这不是最后一个 book, 而是过程中创建的 book
            False: 表示这是最后一个 book
            为什么要有这个参数?
                一般来说, 当数据量很大时, 会在过程中创建很多 book.
                比如有 50w 条数据, 那么会产生:
                    ~/output/save_book_part1(20w).xls
                    ~/output/save_book_part2(20w).xls
                    ~/output/save_book_part3(10w).xls
                但考虑到现实情况可能有 51w, 51.02w 等, 甚至有不知道总量会是多少的情况.
                那么最后一个 book 包含的数据量可能是个零头, 就没有必要写那么清楚.
                而且在 ExcelWriter 中, 也没有专门计算最后一个 book 装载量的方法.
                所以最好是最后一个 book 不要写容量了.
                is_final 参数就是用来判断是不是最后一个 book 的. 如果是的话, 就不在括号里
                面写容量.
        :return
        """
        postfix = ospath.splitext(self.filepath)[1]
        # self.filepath = '../output/save_book.xls' -> postfix = '.xls'
        if not is_final:
            ofile = self.filepath.replace(
                postfix,
                '_part{}({}w){}'.format(
                    self.bookx, 5 * self.sheetx_limit, postfix
                )  # '.xls' -> '_part1(20w).xls'
            )  # -> ofile = 'output/result_part1(20w).xls'
        else:
            ofile = self.filepath.replace(
                postfix,
                '_part{}{}'.format(self.bookx, postfix)
                # '.xls' -> '_part3.xls'
            )  # -> ofile = 'output/result_part3.xls'
            lk.log(f'excel saved to {ofile}', h='parent')
        return ofile
    
    # ------------------------------------------------
    
    def save(self):
        ofile = self.filepath if self.bookx == 1 else self._get_subbook_name(
            True)
        lk.logt('[ExcelWriter][I1139]', f'excel saved to "{ofile}"',
                h='parent')
        self.book.save(self.filepath)


class ExcelCopy(ExcelWriter):
    
    # noinspection PyMissingConstructor
    def __init__(self, reader, filepath, relay_rowx=False):
        """
        注: 由于 ExcelCopy 未继承 ExcelWriter 的 __init__, 所以需要仿照 ExcelWriter
        .__init__() 配置一遍. 注意二者在配置时的异同.

        ARGS:
            reader: ExcelReader.
            filepath: str. 指定输出路径, 特别的, 允许指认 reader 的路径为输出路径.
            relay_rowx: bool.
                True: 从 reader 的当前激活的 sheet 的已有行数的结尾继续.
                False: 从 reader 的当前激活的 sheet 的第一行继续.
        """
        # 注: 不要有 super.__init__()
        
        # ------------------------------------------------ 与 ExcelWriter 相同的
        
        if filepath.endswith('.xlsx'):
            lk.logt('[W2403]', 'ExcelCopy 不支持 xlsx 格式输出, 将自动转为 xls',
                    h='parent')
            filepath = filepath[:-1]
        
        # 路径配置
        self.filepath = filepath
        
        # 自动化配置
        self.automation = {
            'auto_create_header_in_new_sheet'                   : True,
            'consistent_growing_rowx_when_auto_create_new_sheet': True
        }
        
        # ------------------------------------------------ 与 ExcelWriter 不同的
        
        # excel 配置
        from xlutils.copy import copy
        self.book = copy(reader.book)
        
        # 游标配置
        self.sheetx = reader.sheetx
        self.sheet = self.book.get_sheet(self.sheetx)
        # self.rowx, self.rowx_offset = -1, 0
        
        # 容量设计
        self.rowx_limit, self.sheetx_limit = 50000, 1000
        
        # 是否从 reader 结束的行数继续
        if relay_rowx:
            self.rowx = reader.get_num_of_rows() - 1
            # self.rowx_offset = 0
    
    def activate_sheet(self, sheetx: int):
        self.rowx = 0
        self.sheetx = sheetx
        self.sheet = self.book.get_sheet(sheetx)


# ------------------------------------------------

# noinspection PyUnresolvedReferences
class WorkbookYahei(Workbook):
    
    def __init__(self):
        super().__init__()
        self.get_default_style().font.name = '微软雅黑'
    
    # 重写唯一与 Worksheet 关联的方法: add_sheet()
    def add_sheet(self, sheetname, cell_overwrite_ok=False):
        if not isinstance(sheetname, unicode_type):
            sheetname = sheetname.decode(self.encoding)
        if not Utils.valid_sheet_name(sheetname):
            raise Exception("invalid worksheet name %r" % sheetname)
        lower_name = sheetname.lower()
        if lower_name in self._Workbook__worksheet_idx_from_name:
            raise Exception("duplicate worksheet name %r" % sheetname)
        self._Workbook__worksheet_idx_from_name[lower_name] = len(
            self._Workbook__worksheets)
        self._Workbook__worksheets.append(
            WorksheetYahei(sheetname, self, cell_overwrite_ok))
        return self._Workbook__worksheets[-1]


# noinspection PyUnresolvedReferences
class WorksheetYahei(Worksheet):
    
    def __init__(self, sheetname, parent_book, cell_overwrite_ok=False):
        super().__init__(sheetname, parent_book, cell_overwrite_ok)
        self.lkstyle = XFStyle()
        self.lkstyle.font.name = '微软雅黑'
    
    # 重写所有与写入单元格相关的方法的 style 缺省参数.
    
    def write(self, r, c, label="", style=None):
        self.row(r).write(c, label, style or self.lkstyle)
    
    def write_rich_text(self, r, c, rich_text_list, style=None):
        self.row(r).set_cell_rich_text(c, rich_text_list, style or self.lkstyle)
    
    def merge(self, r1, r2, c1, c2, style=None):
        if c2 > c1:
            self.row(r1).write_blanks(c1 + 1, c2, style or self.lkstyle)
        for r in range(r1 + 1, r2 + 1):
            self.row(r).write_blanks(c1, c2, style or self.lkstyle)
        self._Worksheet__merged_ranges.append((r1, r2, c1, c2))
    
    def write_merge(self, r1, r2, c1, c2, label="", style=None):
        assert 0 <= c1 <= c2 <= 255
        assert 0 <= r1 <= r2 <= 65535
        self.write(r1, c1, label, style or self.lkstyle)
        if c2 > c1:
            self.row(r1).write_blanks(c1 + 1, c2, style or self.lkstyle)
        for r in range(r1 + 1, r2 + 1):
            self.row(r).write_blanks(c1, c2, style or self.lkstyle)
        self._Worksheet__merged_ranges.append((r1, r2, c1, c2))
