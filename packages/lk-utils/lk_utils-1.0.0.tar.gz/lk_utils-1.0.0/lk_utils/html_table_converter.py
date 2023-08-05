import re

from bs4 import BeautifulSoup

from . import exit_ways
from .excel_reader import ExcelReader
from .excel_writer import ExcelWriter
from .lk_logger import lk
from .read_and_write_basic import read_file, write_file


def excel_2_html(ifile, ofile, title='', dialog=False):
    """
    IN: ifile. e.g. 'in.xlsx'
    OT: ofile. e.g. 'out.html'
    
    黑魔法:
        假设待处理的表格中有一列是 url (假设 title 为 'homepage'). 您想要让 url 变成可点击
        的蓝色链接, 并且尽可能简洁地显示, 请这样做:
            header before:
                index  name       homepage
                1      Li, Ming   http://abc.com/li-ming
                2      Lin, Fang  http://abc.com/lin-fang
            header after: (注意 homepage 标题头的变化)
                index  name       homepage|visit me
                1      Li, Ming   http://abc.com/li-ming
                2      Lin, Fang  http://abc.com/lin-fang
                
        前者的生成效果如下:
            <tr>
                <td>1</td>
                <td>Li, Ming</td>
                <td>http://abc.com/li-ming</td>
            <tr>
        后者的生成效果如下:
            <tr>
                <td>1</td>
                <td>Li, Ming</td>
                <td><a href="http://abc.com/li-ming" target="view_window">visit
                me</a></td>
            <tr>
            
        黑魔法使用注意事项:
            1. 链接必须以 'http' 或 'https' 开头
            2. 单个单元格必须有且只有一个链接 (如果有多个, 则不作处理)
            3. 链接所属的标题头必须含 "|" 符号, 您可以使用 "homepage|", 本脚本会使用一个默
            认值: "visit"
    """
    
    reader = ExcelReader(ifile)
    
    if dialog:
        def select_sheet():
            preview = ['\tindex\t|\tsheet name']
            
            for index, sheet_name in enumerate(reader.get_name_of_sheets()):
                preview.append(f'\t{index}\t|\t{sheet_name}')
            
            print('\n'.join(preview))
            cmd = input('请选择您要处理的 sheet 序号 (从零开始数): ')
            
            # noinspection PyBroadException
            try:
                cmd = int(cmd)
                reader.activate_sheet(cmd)
            except Exception:
                exit_ways.main('无法处理您的命令')
        
        select_sheet()
    else:
        pass
    
    # html head
    if title == '':
        title = 'html table converter result'
    
    head = f"""
<head>
    <title>{title}</title>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap
◆.min.css"
          integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz
◆/K68vbdEjh4u"
          crossorigin="anonymous">
</head>
<body>
    <div id="excel-2-html-result" class="container">
        <table class="table table-striped table-hover table-bordered">
    """.replace('\n◆', '')
    tail = """
        </table>
    </div>
</body>
    """
    
    html = [head]
    """
    html 打算按照这个结构来设计:
        <table>
            <tbody>
                <tr>  # 第一个 tr 是 header
                    <th>...<th>
                    <th>...<th>
                    <th>...<th>
                </tr>
                <tr>
                    <td>...</td>
                    <td>...</td>
                    <td>...</td>
                </tr>
                <tr>
                    <td>...</td>
                    <td>...</td>
                    <td>...</td>
                </tr>
                ...
            </tbody>
        </table>
    """
    
    detecter = None
    
    for rowx in range(reader.get_num_of_rows()):
        row = reader.row_values(rowx)
        
        if rowx == 0:
            detecter = DetectLink(row)
            header = detecter.get_clean_header()
            cells = (f'<th>{x}</th>' for x in header)
        else:
            cells = (f'<td>{detecter.detect_link(i, x)}</td>'
                     for i, x in enumerate(row))
        
        row = '<tr>{}</tr>'.format('\n'.join(cells))
        html.append(row)
    
    html.append(tail)
    
    # TODO: 整理一下 html, 使美观.
    
    write_file(html, ofile)


class DetectLink:
    
    def __init__(self, header):
        self.link_title = {}
        self.clean_header = []
        
        for index, cell in enumerate(header):
            if '|' in cell:
                a, b = cell.split('|', 1)
                # 'homepage|visit me' -> ['homepage', 'visit me']
                self.clean_header.append(a)
                self.link_title[index] = b if b else 'visit'
                """
                -> self.link_title = {
                    3: 'visit me',
                    4: 'visit',
                }
                """
            else:
                self.clean_header.append(cell)
        # lk.logt('[TEMPRINT]', self.link_title)
        
        self.reg = re.compile(r'https?://')
    
    def get_clean_header(self):
        return self.clean_header
    
    def detect_link(self, index, cell):
        if not self.link_title:
            return cell
        
        if not isinstance(cell, str):
            return cell
        
        if index not in self.link_title:
            return cell
        
        found = self.reg.findall(cell)  # 检测是否包含链接特征
        # lk.logt('[TEMPRINT]', cell, found)
        
        if len(found) != 1:
            # 暂不支持处理 len == 0 或 len > 1 的情况.
            return cell
        else:
            return '<a href="{}" target="view_window">{}</a>'.format(
                cell, self.link_title[index]
            )


# ------------------------------------------------

def html_2_excel(ifile, ofile):
    """
    IN: ifile. e.g. 'in.html'
    OT: ofile. e.g. 'out.xlsx'
    NOTE: 为确保提取效果, 请预先保证 html 中只有一个 <table>.
    """
    try:
        soup = BeautifulSoup(read_file(ifile), 'html.parser')
    except UnicodeDecodeError:
        exit_ways.main('UnicodeDecodeError. please make sure the target file '
                       'should be encoded with "utf-8"', 5)
        return
    
    # 找到 html 中的所有 <table>. 如果存在 <table> 嵌套的现象, 则只取子 table.
    tables = [i for i in soup.find_all('table')
              if not i.find('table') and i.text.strip()]
    # lk.logt('[TEMPRINT]', len(tables))
    """
    过滤方法解决以下两个问题:
        1. `not i.find('table')` 表示此 table 不含子 table
        2. `i.text.strip()` 表示 table 的内容是非空的
    """
    if not tables:
        exit_ways.main('未能在目标文件中发现表格, 请检查输入文件是否有误')
        return
    
    # ------------------------------------------------
    
    writer = ExcelWriter(ofile)
    
    global rowsplug, merge
    rowsplug = {}  # {rowx: [pos]}
    merge = []
    
    for tablex, table in enumerate(tables, 1):
        if tablex > 1:
            writer.add_new_sheet(f'sheet {tablex}')
        
        for rowx, row in enumerate(table.find_all('tr')):
            row_values = get_row_values(rowx, row)
            # lk.loga(rowx, row_values, h='parent')
            writer.writeln(*row_values)
    
    for i in merge:
        writer.merge_cells(*i)
    
    writer.save()


def get_row_values(rowx, row):
    """
    GLOBALS:
        merge: [(x1, y1, x2, y2, data), ...]
        rowsplug: dict. {rowx: [pos]}
    """
    es = row.find_all('td') or row.find_all('th')
    row_values = []

    for pos in rowsplug.get(rowx, []):
        es.insert(pos, None)
    
    for colx, e in enumerate(es):
        if e is None:
            row_values.append(None)
            continue
        
        try:
            span1 = int(e['colspan'])
        except (TypeError, KeyError):
            span1 = 1
        try:
            span2 = int(e['rowspan'])
        except (TypeError, KeyError):
            span2 = 1
        # | span1, span2 = int(getattr(e, 'colspan')) or 1, \
        # |                int(getattr(e, 'rowspan')) or 1

        col_offset = len(row_values)
        value = clean(e.text)
        
        # update merge range
        if span1 > 1 or span2 > 1:
            row_values.extend([None] * span1)
            merge.append(
                (rowx, col_offset,
                 rowx + span2 - 1, len(row_values) - 1,
                 value)
            )
            lk.loga('merge cell', merge[-1], h='grand_parent')
        else:
            row_values.append(value)
            
        # update rowsplug
        if span2 > 1:
            for i in range(col_offset, len(row_values)):  # colx
                for j in range(rowx, rowx + span2):  # rowx
                    node = rowsplug.setdefault(j, [])
                    node.append(i)
        
    return row_values


def clean(value):
    """
    处理:
    1. 删除换行符
    2. 特殊字符变为空格
    3. 去除前后空字符串
    4. 对中文之间的空格删除, 例如 "张 三" 变成 "张三", 且保护英文的 "zhang san" 不会变成
    "zhangsan"
    """
    reg1 = re.compile(r'\n')  # '\n' -> ''
    reg2 = re.compile(r'\s+')  # '  ' -> ' '
    reg3 = re.compile(r'(?<=[\u4e00-\u9fa5]) (?=[\u4e00-\u9fa5])')  # '张 三' ->
    # '张三'
    
    value = re.sub(reg1, '', value)
    value = re.sub(reg2, ' ', value)
    value = re.sub(reg3, '', value)
    
    return value.strip()
