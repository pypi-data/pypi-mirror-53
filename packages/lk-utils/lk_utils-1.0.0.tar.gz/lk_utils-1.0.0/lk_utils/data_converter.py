def json_2_excel(ifile='../temp/in.json', ofile='../temp/out.xls',
                 header=None, auto_index=False):
    from .excel_writer import ExcelWriter
    from .read_and_write_basic import read_json
    
    reader = read_json(ifile)
    writer = ExcelWriter(ofile)
    if header:
        writer.writeln(*header)
    
    for k, v in reader.items():
        writer.writeln(k, v, auto_index=auto_index)
    
    writer.save()


def excel_2_json(ifile='../temp/in.xlsx', ofile='../temp/out.json',
                 key='index'):
    """
    将 excel 转换为 json.
    ARGS:
        ifile
        ofile
        key: 主键依据. 默认是行号, 因为行号是不重复的, 适合作为字典的键. 您也可以定义表格中的某
            个字段为主键. 另外, 如果 key 设为空字符串, 则以列表形式输出每一行.
    IN: ifile
    OT: ofile
    """
    from .excel_reader import ExcelReader
    from .lk_logger import lk
    from .read_and_write_basic import write_json
    
    reader = ExcelReader(ifile)
    writer = {}
    
    if key == 'index':
        if key not in reader.get_header():
            mode = 0
        else:
            mode = 1
    elif key == '':
        # 如果 key 为空字符串, 则以列表形式输出每一行
        writer = tuple(reader.row_values(rowx) for rowx in reader.get_range(1))
        write_json(writer, ofile)
        return
    else:
        mode = 2
    
    for rowx in reader.get_range(1):
        row = reader.row_dict(rowx)
        
        if mode == 0:
            writer[rowx] = row
        elif mode == 1:
            writer[row['index']] = row
        elif mode == 2:
            # noinspection PyBroadException
            try:
                writer[row[key]] = row
            except Exception:
                lk.logt(
                    '[W0536]', 'cannot convert this row because of KeyError',
                    row, key, h='parent'
                )
    
    write_json(writer, ofile)


def excel_2_json_kv(ifile='../temp/in.xlsx', ofile='../temp/out.json',
                    header=False):
    """
    将 excel 转换为 json 文件. 要求 excel 只有两列数据 (占据第一, 第二列位置), 且目标数据位
    于 sheet 1. 最后转换的结果是以第一列为 keys, 第二列为 values.
    """
    from .excel_reader import ExcelReader
    from .read_and_write_basic import write_json
    
    reader = ExcelReader(ifile)
    
    offset = 0 if header else 1
    
    writer = {k: v for k, v in zip(
        reader.col_values(0, offset),
        reader.col_values(1, offset)
    )}
    
    write_json(writer, ofile)
