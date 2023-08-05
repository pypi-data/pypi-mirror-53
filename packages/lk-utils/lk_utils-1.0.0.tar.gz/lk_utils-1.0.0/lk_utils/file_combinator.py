import os

import xlrd

from . import read_and_write_basic
from .excel_writer import ExcelWriter
from .file_sniffer import find_files, get_curr_dir, prettify_dir
from .lk_logger import lk


def combine_txt(idir, trim_header=True):
    sum_file = idir + 'result.txt'
    
    if os.path.exists(sum_file):
        cmd = input('[INFO][file_combinator] the sum file ({}) already exists, '
                    'do you want to overwrite it? (y/n) '.format(sum_file))
        if cmd == 'y':
            pass
        else:
            lk.logt('[I0838]', 'please delete the sum file and retry',
                    h='parent')
            raise AttributeError
    
    files = os.listdir(idir)
    
    writer = read_and_write_basic.FileSword(
        sum_file, 'a', clear_any_existed_content=True)
    
    for f in files:
        if '.txt' in f and f != 'result.txt':
            f = idir + f
            content = read_and_write_basic.read_file(f).strip()
            writer.write(content)
    
    writer.close()
    
    if trim_header:
        from re import compile
        content = read_and_write_basic.read_file(sum_file)
        header = compile(r'^[^\n]+').search(content).group()
        content = content.replace(header + '\n', '')
        content = header + '\n' + content
        read_and_write_basic.write_file(content, sum_file)


def combine_csv(idir='', ofile='result.xls', module=True, ignore=None):
    import csv
    
    if not idir:
        idir = get_curr_dir()
    else:
        idir = prettify_dir(idir)
    
    writer = ExcelWriter(idir + ofile)
    header = False
    
    # ----------------------------------------------------------------
    
    files = find_files(idir, '.csv', return_full_path=False)
    
    for f in files:
        if f == ofile or (ignore and f in ignore):
            continue
        
        lk.logax(f, h='parent')
        
        with open(idir + f, newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile)
            
            for index, row in enumerate(spamreader):
                if index == 0:
                    if header:
                        continue
                    else:
                        header = True
                if module:
                    if index == 0:
                        row = ['module'] + row
                    else:
                        row = [f.split('.')[0]] + row
                writer.writeln(*row)
    
    writer.save()


def combine_excel(idir='', ofile='result.xlsx', module=True, ignore=None,
                  one_sheet=True):
    """
    将指定目录中的所有表格文件合并为一个 result.xlsx.

    IN: 指定一个目录
    OT: 在该目录下生成一个 result.xlsx

    注:
        1. 如果该目录下已经有一个 result.xlsx, 则会自动跳过这个文件, 并将在合并其他文件后覆盖
        此文件
        2. 不支持寻找子目录中的文件
        3. 您可以指定生成的文件名 (即将 result 改成其他), 但请确保后缀名是 xlsx
    """
    if not idir:
        idir = get_curr_dir()
    else:
        idir = prettify_dir(idir)
    
    writer = ExcelWriter(idir + ofile, sheetname='' if one_sheet else None)
    header_on = False
    modulex = 0
    
    # --------------------------------
    
    def exclude_ignored_files(f):
        if f in files:
            files.remove(f)
    
    files = find_files(idir, '.xls', False)
    
    exclude_ignored_files(ofile)
    if ignore:
        if isinstance(ignore, str):
            exclude_ignored_files(ignore)
        else:
            for i in ignore:
                exclude_ignored_files(i)
    
    for exl in lk.wrap_counter(files):
        modulex += 1
        lk.logax(modulex, exl, h='parent')
        
        filename = exl.split('.', 1)[0]
        
        book = xlrd.open_workbook(idir + exl)
        sheet = book.sheet_by_index(0)
        
        if one_sheet:
            if not header_on:
                header_on = True
                
                if module:
                    header = ['module'] + sheet.row_values(0)
                else:
                    header = sheet.row_values(0)
                
                writer.writeln(*header)
        else:  # 分 sheet 模式
            if module:
                header = ['module'] + sheet.row_values(0)
            else:
                header = sheet.row_values(0)
            
            writer.add_new_sheet(modulex)
            writer.writeln(*header)
            """
            为什么 modulex 不使用 module_name 表示?
                1. excel 的 sheet 命名有长度限制, 不能超过 31 个字符
                2. sheet 命名不能有重名
                3. sheet 命名不能有特殊字符
            因此, 如果用 module name 来命名, 可能会报错. 所以采用安全的做法.
            """
        
        for rowx in range(1, sheet.nrows):
            if module:
                writer.writeln(filename, *sheet.row_values(rowx))
            else:
                writer.writeln(*sheet.row_values(rowx))
    
    writer.save()
