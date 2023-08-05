import unicodedata
from re import compile, sub

from .lk_logger import lk

"""
punctuations = {
    'en': r',.:;!?"\'`^+-*/\%<=>@#$&_()[]{}|~',
    'cn_all': '，。、：；！？·“”‘’（）【】《》—…',
    'cn': '，。、：；！？·',
    'cn_pair': ('“”', '‘’', '（）', '【】', '《》'),
    'cn_double': ('——', '……')
}

simple_accents 指 strip_accents() 能自主处理的. 这里仅做兴趣收集 (未来可能会发布为字典),
目前并没有应用的打算.

simple_accents = {
    'á' : 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a',
    'À' : 'A', 'Â': 'A', 'Å': 'A', 'Ä': 'A', 'Ǻ': 'A', 'Ã': 'A', 'À': 'A',
    'Á' : 'A',
    'ç' : 'c', 'ć': 'c', 'č': 'c',
    'Ç' : 'C', 'Č': 'C',
    'é' : 'e', 'è': 'e', 'ê': 'e', 'ě': 'e', 'ë': 'e',
    'É' : 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
    'ǵ' : 'g', 'ǧ': 'g',
    'í' : 'i', 'ï': 'i', 'î': 'i', 'ı': 'i',
    'Î' : 'I', 'Ï': 'I', 'Ì': 'I', 'İ': 'I',
    'ł' : 'l', 'ĺ': 'l',
    'm̈': 'm',
    'ñ' : 'n', 'ń': 'n',
    'ó' : 'o', 'ô': 'o', 'ö': 'o', 'ő': 'o', 'ø': 'o', 'õ': 'o', 'ò': 'o',
    'Ô' : 'O', 'Ö': 'O', 'Ø': 'O',
    'ú' : 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
    'Ù' : 'U', 'Û': 'U', 'Ū': 'U',
    'š' : 's', 'ś': 's',
    'Š' : 'S', 'Ş': 'S',
    'ý' : 'y',
    'ž' : 'z', 'ż': 'z',
    'Ž' : 'Z',
    'œ' : 'oe', 'æ': 'ae',
    'Œ' : 'CE', 'Æ': 'AE',
    'ß' : 'ss',
}

"""


class DiacriticalMarksCleaner:
    """
    变音符号清理.
    
    注意事项:
        本模块对 "ü" 将转换为 "u". 如果您在进行中国人名的转换, 请预先将待处理的文本中的 "ü"
        自处理为 "v".
    """
    strict_mode = False
    
    # 变音符号转换字典
    # 注: 这里的变音符号, 仅收集 strip_accents() 无法处理的部分. 例如 ø -> o,
    # strip_accents() 是做不到的, 所以在这里记为字典.
    cedilla_dict = {
        'ҫ': 'c',
        'đ': 'd',
        'Đ': 'D',
        'ƒ': 'f',
        '¡': 'i',
        'ı': 'i',
        'ł': 'l',
        'Ł': 'L',
        'ø': 'o',
        'Ø': 'O',
        'æ': 'ae',
        'œ': 'oe',
        'Æ': 'AE',
        'Œ': 'CE',
        'ß': 'ss',
    }
    
    symbol_dict = {
        '‘': "'", '’': "'", "ʼ": "'",
        # '#': '', '*': '',
        '¨': ' ', "ˇ": " ", "´": " ",
        "°": "°",
        '÷': '/',
        '†': '',
        '¼': '1/4', '³': '3'
    }
    
    reg1 = compile(r'\s')
    reg2 = compile(r' +')
    reg3 = compile(r"[^-~()\[\]@'\",.:;?! "
                   r"a-zA-Z0-9"
                   r"\u4e00-\u9fa5"
                   r"\u0800-\u4e00"
                   r"\uAC00-\uD7A3]")
    
    def __init__(self, custom_dict=None):
        if custom_dict:
            self.symbol_dict.update(custom_dict)
    
    @staticmethod
    def strip_accents(text):
        """
        去除变音符号.
        
        IO: Ramírez Sánchez -> Ramirez Sanchez
        
        NOTE: this works fine for spanish, but not always works for other
        languages (e.g. ø -> ø). so i'll prepare another dict to handle the
        latter ones (see self.cedilla_dict).
        
        REFER: https://stackoverflow.com/questions/4512590/latin-to-english
        -alphabet-hashing
        """
        # if 'ü' in text:
        #     text = text.replace('ü', 'v')
        return ''.join(
            char for char in unicodedata.normalize('NFKD', text)
            if unicodedata.category(char) != 'Mn'
        )
    
    def main(self, word, trim_symbols=True):
        if not word:
            return ''
        else:
            return self.trans(word, trim_symbols)
    
    def trans(self, word, trim_symbols=True):
        word = sub(self.reg1, ' ', word)
        
        for k, v in self.cedilla_dict.items():
            word = word.replace(k, v)
        
        word = self.strip_accents(word)
        
        if trim_symbols:
            for k, v in self.symbol_dict.items():
                word = word.replace(k, v)
        
        if self.strict_mode:
            x = self.reg3.findall(word)
            if x:
                lk.logt('[W2557]', 'found uniq and unreg symbol', word, x,
                        h='parent')  # uniq: unique; unreg: unregisted
                word = sub(self.reg3, '', word)
        
        word = sub(self.reg2, ' ', word)
        return word.strip()


class PunctuationConverter:
    cn_to_en = {
        '，' : ', ',
        '。' : '. ',
        '“' : '"',
        '”' : '"',
        '‘' : '\'',
        '’' : '\'',
        '：' : ': ',
        '；' : '; ',
        '、' : ', ',
        '·' : ' ',
        '~' : '~',
        '？' : '? ',
        '！' : '! ',
        '（' : ' (',
        '）' : ') ',
        '【' : '[',
        '】' : ']',
        '《' : '"',
        '》' : '"',
        '……': '...',
        '——': ' - ',
    }
    """
    punctuations = {
        'en': r',.:;!?"\'`^+-*/\%<=>@#$&_()[]{}|~',
        'cn_all': '，。、：；！？·“”‘’（）【】《》—…',
        'cn': '，。、：；！？·',
        'cn_pair': ('“”', '‘’', '（）', '【】', '《》'),
        'cn_double': ('——', '……')
    }
    """
    
    def __init__(self):
        pass
    
    def main(self, q):
        return self.trans(q.strip()) if q else ''
    
    def trans(self, q):
        for k, v in self.cn_to_en.items():
            q = q.replace(k, v)
        q = sub(' +', ' ', q.strip())
        return q


def discover(ifile, ofile):
    from . import read_and_write_basic
    
    transer = DiacriticalMarksCleaner()
    transer.strict_mode = False
    reg = transer.reg3
    
    ilist = read_and_write_basic.read_file_by_line(ifile)
    ilist2 = []
    
    for i in ilist:
        for j in reg.findall(i):
            if j not in ilist2:
                ilist2.append(j)
    
    odict = {}
    
    for i in ilist2:
        odict[i] = transer.main(i)
    
    read_and_write_basic.write_json(odict, ofile)


if __name__ == '__main__':
    discover('in.txt', 'out.json')
