import os, sys
import subprocess
import time
import random, hashlib, urllib.parse
import requests

PATH = 'content'
type_ = 'resTructured' # Markdown
FILENAME = '%Y-%m-%d-{title}'


def main():
    argv = sys.argv

    if len(argv) > 1:
        make(argv)

def make(argv):
    if len(argv) > 1:
        if argv[1] == 'create':
            return create(argv)
        else: return None

def create(argv):
    '''
    创建指定的文章
    '''
    if len(argv) > 2:
        filename = (time.strftime(FILENAME, time.localtime())).format(title=argv[2])
        content = argv[2] + '\n' + (len(argv[2])+1)*'=' + '\n:date: '+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n:slug: ' + translation(argv[2])

        ext = '.rst' if type_ == 'resTructured' else '.md'
        with open(PATH+'/'+filename+ext, 'w') as fp:
            fp.write(content)

def translation(query, from_ = 'auto', to = 'en'):
    '''
    请求百度翻译 api 获取翻译结果
    '''
    appid = '20161217000034172'
    secretKey = '07Qh2zEwKIx3kGwer1Uz'
    salt = random.randint(32768, 65536)
    sign = appid+query+str(salt)+secretKey
    m1 = hashlib.md5(sign.encode('utf8'))
    sign = m1.hexdigest()
    url ='http://api.fanyi.baidu.com/api/trans/vip/translate?'
    url = url + urllib.parse.urlencode({'q':query, 'from':from_, 'to':to, 'appid':appid, 'salt':salt, 'sign':sign})

    r = requests.get(url)
    r.encoding = 'utf-8'
    result = r.json()
    if 'error_code' in result:
        # raise TransLationError
        return None

    if 'trans_result' in result:
        return result['trans_result'][0].get('dst', None)

    return None

if __name__ == '__main__':
    main()
