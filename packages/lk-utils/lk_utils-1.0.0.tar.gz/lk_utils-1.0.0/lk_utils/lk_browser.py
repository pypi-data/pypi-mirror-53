from random import randint
from time import sleep

from requests import Response, Session

from .lk_logger import lk


def launch_browser(cookies=None, header=None) -> Session:
    _browser = Session()
    
    if header is None:
        _browser.headers.update({
            "Accept"         : "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection"     : "keep-alive",
            "User-Agent"     : "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                               "AppleWebKit/537.36 (KHTML, like Gecko) "
                               "Chrome/74.0.3729.169 "
                               "Safari/537.36"
        })  # 更新于2019年6月5日
    else:
        _browser.headers.update(header)
    
    if cookies:
        if isinstance(cookies, str):
            # the variable cookies is a file path
            # so get a dict from this file
            cookies = cook_cookies(cookies)  # type: dict
        elif not isinstance(cookies, dict):
            raise TypeError
        _browser.cookies.update(cookies)
    
    return _browser


def cook_cookies(filepath):
    """
    将从浏览器获得的 cookies 转换成 requests 可用的字典格式.
    
    输入:
        cookies.txt
    输出:
        (json)cookies
    
    cookies.txt 文件从哪里获得?
        打开搜狗浏览器, 按 f12 打开开发者模式, 切换到 network 分页 (如果是空白的, 请按 f5
        刷新页面), 点击其中任意一个连接, 可以看到 cookies 信息.
        将 cookies 复制下来, 放到 'data/cookies.txt' 中即可.
    
    示例: 从搜狗浏览器中复制下来的 cookies 示例:
        __cfduid=d21d1566cd380b98975e8c0017a257; utt=615-465762a6561d42cd22c7;
        SCSessionID=A4450E45...

    参考:
        https://www.jianshu.com/p/5ef0c7bb1ed2
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        read_cookies = f.read().strip(';')
        # -> '__cfduid=d21d1566cd380b98975e8c0017a257; utt=615-465762a6561d42cd2
        # 2c7; SCSessionID=A4450E45...'
    
    cookies = {}
    
    for i in read_cookies.split(';'):
        # -> ['__cfduid=d21d1566cd380b98975e8c0c1017a257', ' utt=615
        # -465762a6561d4d632b5-3fbd2cd22c7', ...]
        k, v = i.strip().split('=', 1)
        '''
        ' utt=615-465762a6561d4d632b5-3fbd2cd22c7' -> 'utt=615-465762a6561d4d632
        b5-3fbd2cd22c7' -> ['utt', '615-465762a6561d4d632b5-3fbd2cd22c7']
        ' WT_FPC=id=24280465122e355edc21555260912336:lv=1555262656515:ss=1555260
        912336' -> 'WT_FPC=id=24280465122e355edc21555260912336:lv=1555262656515:
        ss=1555260912336' -> ['WT_FPC', 'id=24280465122e355edc21555260912336:lv=
        1555262656515:ss=1555260912336']
        '''
        
        if '"' in v:
            # e.g. '"1080:1920"'
            v = v.replace('"', '')  # -> '1080:1920'
        
        cookies[k] = v
        # -> {'__cfduid': 'd21d1566cd380b98975e8c0c1017a257', 'utt': '615
        # -465762a6561d4d632b5-3fbd2cd22c7', ...}
    
    return cookies


# ------------------------------------------------

class LKBrowser:
    # settings
    is_raise_error = False
    sleepy = None  # see self._doze, self.get() and self.post()
    
    # bindings
    response = None
    
    def __init__(self):
        self.session = launch_browser()
    
    # ------------------------------------------------ sleeping
    
    def be_server_friendly(self, sleepy=None):
        self.sleepy = sleepy or (0, 3)
    
    def _doze(self):
        if self.sleepy:
            r = randint(*self.sleepy)
            sleep(r)
    
    # ------------------------------------------------ cookies
    
    @property
    def cookies(self):
        return self.session.cookies
    
    def get_cookies(self) -> dict:
        return self.session.cookies.get_dict()
    
    def set_cookies(self, cookies):
        """
        IN: cookies
                str: 表示一个 cookies 文件的路径. 如果该路径以 '.txt' 结尾, 则使用
                    cook_cookies() 方法读取; 如果是以 '.json' 结尾, 则使用
                    read_json() 方法. 最终目的是将其转化为 dict 类型.
                dict: 可直接使用.
        OT: self.session.cookies (updated)
        """
        if isinstance(cookies, str):
            if cookies.endswith('.txt'):
                cookies = cook_cookies(cookies)
            elif cookies.endswith('.json'):
                from .read_and_write_basic import read_json
                cookies = read_json(cookies)
            else:
                return
        elif isinstance(cookies, dict):
            pass
        else:
            return
        self.session.cookies.update(cookies)
    
    # ------------------------------------------------
    
    def get(self, url, params=None) -> str:
        """
        request of GET method.
        """
        self._doze()
        self.response = self.session.get(url, params=params)
        self._check_status_code()
        return self.response.text
    
    def post(self, url, data) -> str:
        """
        request of POST method.
        """
        self._doze()
        self.response = self.session.post(url, data=data)
        self._check_status_code(data)
        return self.response.text
    
    def postfile(self, url: str, filedata: dict, data=None) -> Response:
        """
        FIXME: maybe we should return response.text
        
        example:
            1. smfile 图床:
                filedata = {'smfile': open('123.png', 'rb)}
                data = {'ssl': False, 'format': 'json'}
            2. chrome 浏览器:
                假设我们在某网页提交时, xhr 链接如下:
                    url: https://example.com/submit
                    method: POST
                    form (点击 view parsed 按钮):
                        authorFile: (binary)
                    form (点击 view source 按钮):
                        ------WebKitFormBoundaryXt7PiZRFs1qj9b46
                        Content-Disposition: form-data; name="authorFile";
                        filename="test.json"
                        Content-Type: application/json
                        
                        
                        ------WebKitFormBoundaryXt7PiZRFs1qj9b46--
                那么这样使用 postfile:
                    browser.postfile(
                        'https://example.com/submit',
                        {'authorFile': open('test.json', 'rb')}
                    )
        参考:
            [崔庆才] Python 3 网络爬虫开发实战.pdf - p142
            https://blog.csdn.net/qq_32502511/article/details/80924090
        """
        self.response = self.session.post(url, files=filedata, data=data)
        return self.response
    
    def download(self, url, ofile):
        """
        注: 此方法不检查下载文件的编码格式
        参考:
            python 爬虫 requests 下载图片 - 稀里糊涂林老冷 - 博客园
            https://www.cnblogs.com/Lin-Yi/p/7640155.html
        """
        self.response = self.session.get(url)
        with open(ofile, 'wb') as f:
            f.write(self.response.content)
    
    def download_text_page(self, url, ofile, encoding='utf-8'):
        """
        这是 self.download() 方法的特化版, 专门用于下载并调节下载文件的格式以 utf-8 保存.
        """
        self.response = self.session.get(url)
        
        """
        注意: 本方法对获取编码的方法进行了调整:
        1. 优先使用 chardet 预测的 encoding, 其次是 http headers 提供的 encoding 信息.
           这样做的原因在于, 经发现国内的一些网站的 http headers 提供的是错误的 encoding.
           比如 http://www.most.gov.cn/cxfw/kjjlcx/kjjl2000/200802/t20080214_5902
           3.htm, 明明含有中文, 但却提供了纯西文字符的 "ISO-8859-1" 编码集, 如果按照 "ISO
           -8859-1" 来解码, 会出现乱码. 而用 chardet 预测的编码 (GB2312) 来解码则不会出现
           乱码
        2. 若 chardet 预测编码为 GB2312, 则使用 GBK 代替. 因为 GBK 是 GB2312 的超集, 且
           国内网站以 GBK 编码的要远多于 GB2312, 使用 GBK 替代不会有任何副作用, 相反能避免部
           分中字符无法解析的情况 (参考: http://ioqq.com/python-chardet-gbk%E8%BD%ACu
           tf8-%E4%B8%AD%E6%96%87%E4%B9%B1%E7%A0%81.html)
        """
        if any(ofile.endswith(x) for x in (  # 常见的二进制文件
                '.exe', '.flv', '.ico', '.jpeg', '.jpg', '.mp3', '.mp4',
                '.mpeg', '.pdf', '.png', '.rar', '.xls', '.xlsx', '.zip'
        )):
            source_encoding = None
        else:
            source_encoding = self.response.apparent_encoding \
                              or self.response.encoding
        target_encoding = encoding
        
        # lk.logt('[TEMPRINT]', source_encoding)
        if source_encoding is None:
            # 出现这种情况, 说明网页没有给出编码信息, chardet 也无法预测. 通常意味着此文件是
            # pdf, jpg, png 等类型的文件. 那么我们采用二进制写入.
            with open(ofile, 'wb') as f:
                f.write(self.response.content)
        else:
            if source_encoding == 'GB2312':
                source_encoding = 'GBK'
            
            content = self.response.content.decode(
                source_encoding, errors='ignore'
            )
            
            with open(ofile, 'w', encoding=target_encoding) as f:
                f.write(content)
    
    # ------------------------------------------------ inner methods
    
    def _check_status_code(self, additional_info=None):
        """
        some serious status code:
            403 permission denied
            429 too frequent requests
        """
        status_code = self.response.status_code
        
        if status_code == 200:
            return
        
        # the following case is assert status_code != 200
        
        h = 'grand_parent'
        info = {
            'error_msg'  : '',
            'status_code': status_code,
            'url'        : self.response.url,
            'extra'      : additional_info
        }
        
        if status_code >= 400:
            if status_code == 403:
                info['error_msg'] = 'permission denied (forbidden)'
            elif status_code == 429:
                info['error_msg'] = 'too frequent requests'
            else:
                info['error_msg'] = 'error 400+'
            lk.logt('[E1512]', info, h=h)
            raise Exception
        else:
            info['error_msg'] = 'unexpected status code'
            lk.logt('[W0114]', info, h=h)
        
        if self.is_raise_error:
            raise Exception
    
    # ------------------------------------------------ properties
    
    @property
    def status_code(self) -> int:
        return self.response.status_code
    
    @property
    def is_redirect(self) -> bool:
        """
        检查是否发生重定向.
        RT: True: 发生了重定向
            False: 没有重定向
        """
        return self.response.is_redirect


# ------------------------------------------------

browser = LKBrowser()
