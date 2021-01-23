"""网络请求的统一接口"""
import re
import requests
import lxml.html


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}


def get_html_text(url, encoding=None):
    """获取指定网页的原始html文本"""
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    r.encoding = encoding if encoding else r.apparent_encoding
    return r.text


def get_html(url, encoding=None):
    """获取指定网页经lxml解析后的document"""
    text = get_html_text(url, encoding=encoding)
    html = lxml.html.fromstring(text)
    return html


def is_url(url: str):
    """判断给定的字符串是否是有效的带协议字段的URL"""
    # https://stackoverflow.com/a/7160778/6415337
    pattern = re.compile(
        r'^(?:http)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|'     #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'      # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(pattern, url) is not None


def is_connectable(url, timeout=3):
    """测试与指定url的连接"""
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False


def download(url, file):
    """下载指定url的资源"""
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    with open(file, 'wb') as f:
        f.write(r.content)


if __name__ == "__main__":
    print(is_connectable('http://www.baidu.com'))