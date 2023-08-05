import re

from .char_converter import DiacriticalMarksCleaner
from .chinese_name_processor import PinyinProcessor


def prettify_name(name: str, lower=True, save_dot=False,
                  soft_comma=True) -> str:
    """
    简化名字格式.
    IO: 'Dong,  Juán-Lang(Esther) T.;' -> 'dong, juan lang esther t'
    
    ARGS:
        name
        lower
        save_dot: bool; default False
            True: 保留点号
            False: 不保留点号, 将被转换为空格
        soft_comma: bool; default True. 主要针对 scopus name 格式的优化
            True: 如果有 'A,B', 则转换为 'A, B'
            False: 不作检查和处理
    
    净化内容:
        1. 将变音字母转为英文字母
            'Doke, Likiánta' -> 'doke, likianta'
        2. 字母全部转为小写 (由 lower 参数控制)
            "Di’Doke, Likianta' -> "di'doke, likianta"
        3. 将括号, 点号, 短横线等转换为空格 (由 reg1 变量控制) (点号由 save_dot 参数控制)
            'doke, l.k.' -> 'doke, l k'
        4. 将多个连续的空格 (或其他不可见字符) 转换为单个空格
            'doke,\tlikianta\n' -> 'doke, likianta '
        5. 将 ',' 转换为 ', ' (由 scopus_name 参数控制)
            'doke,likianta' -> 'doke, likianta'
        6. 去除首尾多余的空格
            'doke, likianta ' -> 'doke, likianta'
    """
    if not name:
        return ''
    
    char_cleaner = DiacriticalMarksCleaner()
    
    reg1_with_dot = re.compile(r'[-~.*\'()]')  # 去除杂乱符号
    reg1_no_dot = re.compile(r'[-~.*\'()]')
    reg2 = re.compile(r'\s+')
    
    # ------------------------------------------------
    
    name = char_cleaner.main(name)
    # 'Doke, Likiánta' -> 'doke, likianta'
    
    if lower:
        name = name.lower()
        # "Di’Doke, Likianta' -> "di'doke, likianta"
    
    if save_dot:
        name = re.sub(reg1_no_dot, ' ', name)
        # 'doke, l.k.' -> 'doke, l.k.'
    else:
        name = re.sub(reg1_with_dot, ' ', name)
        # 'doke, l.k.' -> 'doke, l k '
        # 'doke, liki-anta' -> 'doke, liki anta'
        # "di'doke, likianta" -> "di doke, likianta"
        # 'doke, likianta (lk)' -> 'doke, likianta  lk '
        # ps: 对于残缺的括号也可以处理: 'doke, likianta (lk' -> 'doke, likianta  lk'
    
    name = re.sub(reg2, ' ', name)
    # 'doke,\tlikianta\n' -> 'doke, likianta '
    # 'doke,  likianta' -> 'doke, likianta'
    # ps: 空格也是不可见字符, 所以该步骤可以让多个连续的空格变为一个.
    
    if soft_comma and ',' in name and ', ' not in name:
        name = name.replace(',', ', ')
        # 'doke,likianta' -> 'doke, likianta'
    
    name = name.strip()
    # 'doke, likianta ' -> 'doke, likianta'
    
    return name


def prettify_typo(word: str) -> str:
    """
    优化书写格式.
    注: 仅支持英文符号规则.
    
    IO: 'hi!how  are you? \n' -> 'hi! how are you?'
    """
    if len(word) < 3:
        return word.strip()
        # '' -> '', ' ' -> '', 'A,' -> 'A,', ...
    
    char_cleaner = DiacriticalMarksCleaner()
    
    reg1 = re.compile(r'\s+')
    reg2 = re.compile(r'[,?!:]\w|\.{3}\w|\.\w')  # 注意这里用 \w 而不是 (?=\w)
    reg2_exclude = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', '-')
    reg3 = re.compile(r' +')
    
    # ------------------------------------------------
    
    word = char_cleaner.main(word).lower()
    # 'ÂBC' -> 'abc'
    # "A’BC" -> "A'BC"
    
    word = re.sub(reg1, ' ', word)
    # 'A\tB\n' -> 'A B '
    
    for i in reg2.findall(word):
        if i[-1] in reg2_exclude:
            continue
        word = word.replace(i, i[:-1] + ' ' + i[-1], 1)
        """
        'A,B...C: D!E!F!' -> 'A, B... C: D! E! F!'
        'A,B...C:? D!E!!F!' -> 'A, B... C:? D! E!! F!' (完美处理)
        'π=3.1415' -> 'π=3.1415'
        
        注: 以下情况不作处理:
            1. 连接符. 比如 'Sun, Yat-Sun' 和 'Chrome - Help', 保持原样 (也就是这两种情
            况都是允许的, 甚至允许共存)
            2. 小数点, 比如 '3.14', 保持原样
            3. 运算符号 (+ - x / = % 等) 保持原样
        """
    
    word = re.sub(reg3, ' ', word)
    # 'A  B' -> 'A B'
    
    if ',' in word and ', ' not in word:
        word = word.replace(',', ', ')
        # 'doke,likianta' -> 'doke, likianta'
    
    word = word.strip()
    # 'A ' -> 'A'
    
    return word


def formatify_filename(filename):
    """
    传入一个未处理的文件名, 将其中可能含有的 windows 路径不支持的符号去除后返回.
    其他: 为了使命名美观, 提高一致性, 以及降低文件名和目录的混淆, 本方法会额外做以下事情:
        1. 将变音字符转换为英文字母
        2. 将 "'" 转为空字符
        3. 将 "." 转为空字符或空格 (目前采用空字符)
        4. 将多个连续的空格转为单个空格
        5. 去除首尾多余的空格
    注意: 请不要在参数 filename 中包含后缀, 否则会导致后缀名被破坏.
    
    IO: 'Race's W.' -> 'Races W'
    """
    # windows 文件名不支持的符号有: * : / \\ ? < > { } | "
    reg1 = re.compile(r'[*:/\\?<>{}|"\']')
    reg2 = re.compile(r'\s+')
    char_cleaner = DiacriticalMarksCleaner()
    
    filename = char_cleaner.main(filename).replace("'", '').replace(".", '')
    filename = re.sub(reg1, ' ', filename)
    filename = re.sub(reg2, ' ', filename).strip()
    
    return filename


# ----------------------------------------------------------------

pinyin_processor = PinyinProcessor(wade_mode=True)


def lastfirst_2_firstlast(name: str) -> str:
    """
    将姓前名后的格式转换为名前姓后. (将 scopus_name 格式转换为 name_en)
    NOTE:
        lastfirst_2_firstlast() 与 firstlast_2_lastfirst() 存在显著的不同. 本方法更加
        简单.
        调用者请注意捕捉 ValueError, 其产生原因为 name 参数不含 ', '.
    """
    m, n = name.split(', ', 1)
    return f'{n} {m}'


translator = DiacriticalMarksCleaner()
translator.strict_mode = True


def firstlast_2_lastfirst(name: str) -> str:
    """
    将名前姓后的格式转换为姓前名后. (将 name_en 转换为 scopus_name 格式)
    
    IO: `firstname lastname` -> `lastname, firstname`
        rules:
            1. 输出时, 会一律转换为全小写
            2. 对于变音字母, 转换为普通字母
            3. 可以识别复姓
        examples:
            'Albert Einstein' -> 'einstein, albert'
            'Jieming Hu' -> 'hu, jieming'
            'Enrique von Martz' -> 'von martz, enrique'
            'Carlos Cruz-Coke' -> 'cruz-coke, carlos'
            'Jesus Martinez De La Fuente' -> 'de la fuente, jesus martinez'
    
    about double surnames
        alias:
            double-barrelled surname
            hyphenated surname
            two-part surname
            alliance names (normal in Germany, not heritable)
            allianznamen (normal in Germany, not heritable)
        refer:
            http://www.city-data.com/forum/genealogy/2476579-two-part-surnames
            -like-van-del.html
            https://en.wikipedia.org/wiki/Double-barrelled_name
    """
    # 外国人名中, "复姓" 的情况
    surname_double = (
        'al', 'da', 'de', 'del', 'della', 'demarco', 'den', 'der', 'di', 'dr', 
        'du', 'el', 'jr', 'junior', 'la', 'le', 'los', 'mc', 'mac', 'o', "o'",
        'saint', 'van', 'von',
    )
    
    name = translator.main(name.lower().replace(' - ', '-').strip('-'))
    # 'A B-' -> 'a b', 'A - B' -> 'a-b'
    
    if ' ' not in name:
        name += ', x'
        return name
    
    a, b = name.rsplit(' ', 1)
    a = a.replace('-', ' ')
    count = 0
    while ' ' in a:
        count += 1
        if count == 3:
            break
        
        c, d = a.rsplit(' ', 1)
        if count == 1:
            if b in surname_double or d in surname_double:
                b = d + ' ' + b
                a = c
                continue
        else:
            if d in surname_double:
                b = d + ' ' + b
                a = c
                continue
        break
    
    name = f'{b}, {a}'
    return name


# ------------------------------------------------

def name_str_to_dict(name: str) -> dict:
    """
    将传入的 str 类型的 scopus_name 转换为字典格式.

    注: 传入的姓名必须是 "last, first middle" 格式.
    
    IN: e.g. 'di castelnuovo, augusto f'
    OT: {
            'name': 'di castelnuovo, augusto f',
            'ischinese': False,
            'lastname': 'di castelnuovo',
            'firstname0': 'augusto f',
            'firstname': 'augusto',
            'middlename': 'f'
        }
    """
    
    name = name.replace('.', '').replace('-', ' ').lower()
    
    lastname, firstname0 = name.split(', ')
    # firstname0 是除姓以外的所有部分, 相当于 "名 + 中间名"
    # 这里可能会报 ValueError (name splitting failed), 注意捕捉
    
    ischinese = pinyin_processor.is_chinese(name)
    if ischinese:
        x = pinyin_processor.cut_pinyin(firstname0)  # type: list
        # e.g. 'taiping thomas' -> ['tai', 'ping', 'thomas']
        firstname0 = ' '.join(x)
    
    def simple_split_firstname0(y):
        """
        简单切分名字和中间名, 按照空格来切.
        """
        if ' ' not in y:
            return y, ''
        return y.split(' ', 1)
    
    firstname, middlename = simple_split_firstname0(firstname0)
    
    namedict = {
        'name'      : name,
        'ischinese' : ischinese,
        'lastname'  : lastname,
        'firstname0': firstname0,
        'firstname' : firstname,
        'middlename': middlename
    }
    
    return namedict
