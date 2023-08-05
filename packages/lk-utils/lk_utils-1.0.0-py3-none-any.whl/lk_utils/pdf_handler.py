from .lk_logger import lk


def pdf_to_txt(ifile, ofile, page_start=0, page_end=0):
    """
    IN: ifile
    OT: ofile
    
    ARGS:
        ifile: ends with '.pdf'
        ofile: ends with '.xlsx'
        page_start: starts with 0
        page_end: zero means auto detecting all pages
    
    NOTE:
        1. 本函数需要安装 pdfminer 模块
        2. python 3.x 需要安装的是 pdfminer3k 而不是 pdfminer (后者仅支持 python 2.x),
        不过在导入的时候的语句都是 `import pdfminer`
        3. 本函数不支持将 pdf 中的表格保留原结构 (每一个单元格中的内容将会被逐行输出). 如有需
        求请使用 pdf_2_excel()
    
    REF: Python 3.6 中使用 pdfminer 解析 pdf 文件 - 大泡泡的专栏 - CSDN博客
    https://blog.csdn.net/u011389474/article/details/60139786
    """
    from pdfminer.converter import PDFPageAggregator
    from pdfminer.layout import LAParams, LTTextBoxHorizontal
    from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
    from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
    from pdfminer.pdfparser import PDFDocument, PDFParser
    
    # ------------------------------------------------
    
    writer = open(ofile, 'a', encoding='utf-8')
    
    # 以二进制读模式打开
    reader = open(ifile, 'rb')
    # 用文件对象来创建一个 pdf 文档分析器
    parser = PDFParser(reader)
    # 创建一个 pdf 文档
    doc = PDFDocument()
    # 连接分析器与文档对象, 这个语句比较有意思, 相互 set 对方进去
    parser.set_document(doc)
    doc.set_parser(parser)
    
    # 提供初始化密码. 如果 pdf 没有密码, 就传入一个空参数
    doc.initialize()
    
    # 检测文档是否提供 txt 转换, 不提供就忽略
    if not doc.is_extractable:
        # 如果 pdf 不支持提取, 则直接报错
        raise PDFTextExtractionNotAllowed
    else:
        # 创建 pdf 资源管理器来管理共享资源
        manager = PDFResourceManager()
        # 创建一个 pdf 设备对象
        device = PDFPageAggregator(manager, laparams=LAParams())
        # 创建一个 pdf 解释器对象
        interpreter = PDFPageInterpreter(manager, device)
        
        # 循环遍历列表, 每次处理一个 page 的内容
        pages = list(doc.get_pages())
        if page_end == 0:
            page_end = len(pages)
        
        for i in range(page_start, page_end):
            interpreter.process_page(pages[i])
            
            # 接受该页面的 LTPage 对象
            layout = device.get_result()
            # 这里返回的是一个 LTPage 对象, 里面存放着这个 page 解析出的各种对象
            # 一般包括 LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就取它的 text 属性, 即 x.get_text()
            
            # 获取 text 属性
            for x in layout:
                if isinstance(x, LTTextBoxHorizontal):
                    results = x.get_text()
                    writer.write(results + '\n')
        
        # 最后关闭读写器
        reader.close()
        writer.close()


def pdf_to_excel(ifile, ofile, page_start=0, page_end=0, indicator=True):
    """
    IN: ifile
    OT: ofile
    
    ARGS:
        ifile: postfixed with '.pdf'
        ofile: postfixed with '.xlsx'
        page_start: count from 0
        page_end: 0 means 'auto detect all pages'
        indicator: True means adding pageno, tableno and lineno fields
    
    NOTE:
        1. 本函数需要安装 pdfplumber 模块 (pip install pdfplumber)
        2. 注意 pdfplumber 所依赖的 pdfminer.six 与 pdfminer3k 包名冲突. 这导致本函数与
        pdf_to_txt() 只有一个可以工作 (2019年9月18日), 未来会删除 pdfminer3k, 全系使用
        pdfminer.six
    
    REF: https://www.jianshu.com/p/f33233e4c712
    """
    import pdfplumber
    from lk_utils.excel_writer import ExcelWriter
    
    reader = pdfplumber.open(ifile)
    writer = ExcelWriter(ofile)
    
    if indicator:
        writer.writeln('pageno', 'tableno', 'lineno')
    
    if page_end == 0:
        pages = reader.pages[page_start:]
    else:
        pages = reader.pages[page_start:page_end]
    
    pageno = tableno = lineno = 0
    
    for p in pages:
        pageno += 1
        lk.logd(f'pageno = {pageno}, lineno = {lineno}', h='parent')
        for table in p.extract_tables():
            tableno += 1
            for row in table:
                lineno += 1
                if indicator:
                    writer.writeln(pageno, tableno, lineno, *row)
                else:
                    writer.writeln(*row)
    
    reader.close()
    writer.save()
