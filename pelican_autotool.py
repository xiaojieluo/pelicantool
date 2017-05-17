import os, sys
import subprocess
import time
import random, hashlib, urllib.parse
import requests
import re
import yaml

PATH = 'content'
type_ = 'resTructured' # Markdown
FILENAME = '%Y-%m-%d-{title}'
AUTHOR = 'xiaojieluo'

class Autotool(object):
    '''
    pelican 自动化管理工具
    自动根据指定格式生成文章
    通过百度翻译 API 获取 slug

    程序会从三个地方获取运行参数
        1. 命令行手动指定参数
        2. 从当前目录的 pelican_autotool.yaml 文件中读取配置
        3. 从当前目录的 pelicanconfig.py 文件中读取配置
    优先级为 1 > 2 > 3,遇到相同的参数则覆盖
    '''
    def __init__(self, argv):
        self.argv = argv
        self.data = {
            'create':'','author':'','path':self.get_path(),'type':'','author':'','filename':'%Y-%m-%d-{title}'
        }
        # if self.data.get('path') == '':
        #     self.data['path'] = self.get_path()
        self.data.update(self._get_conf())

    def _get_conf(self):
        '''
        从 yaml 文件中读取 pelican_autotool 的配置信息,覆盖默认参数
        '''
        filename = 'pelican_autotool.yaml'

        if (os.path.exists(filename)):
            with open(filename) as fp:
                try:
                    return yaml.load(fp)
                except yaml.YAMLError:
                    print("yaml 配置文件错误")
                    print(dir(yaml.YAMLError.args))
                    return {}
        else:
            return {}

    def show_help(self):
        print("==================\n")
        print("Usage: pelican_autotool [OPTION]... [FILE]... \nList information about the FILEs (the current directory by default). \nSort entries alphabetically if none of -cftuvSUX nor --sort is specified.\n")

    def run(self):
        '''
        解析命令行参数,并将相应参数赋值到对应变量中
        '''
        if 'help' in self.argv:
            self.show_help() # 显示帮助信息之后退出程序
            return
        if '-a' in self.argv:
            self._get_para(self.argv.index('-a'), 'author')
        if '-p' in self.argv:
            self._get_para(self.argv.index('-p'), 'path')
        if '-t' in self.argv:
            self._get_para(self.argv.index('-t'), 'type')
        if 'create' in self.argv:
            self._get_para(self.argv.index('create'), 'create')
            self.create(self.argv)
            return

    def _get_para(self, index, name):
        '''
        内部函数,将解析出来的参数保存到 self.data 字典中
        '''
        if len(self.argv) > index+1:
            self.data[name] = self.argv[index+1]
        else:
            # self.data[name] = ''
            print("参数不完整")
            # return None

    def create(self,argv):
        '''
        创建指定的文章
        '''
        if self.data.get('create'):
            filename = (time.strftime(FILENAME, time.localtime())).format(title=self.data.get('create'))
            content = self.data.get('create') + '\n' + (len(self.data.get('create'))+2)*'=' + \
                    '\n:date: '+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + \
                    '\n:slug: ' + replace(self.translation(self.data.get('create'))) + \
                    '\n:modified: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + \
                    '\n:author: ' + self.data.get('author')

            ext = '.rst' if (self.data.get('type') == ('rst' or 'resTructured'))  else '.md'
            fullname = os.path.join(self.data.get('path'), filename)+ext
            
            # 目录不存在,则创建
            if os.path.isdir(os.path.join('./',self.data.get('path'))) is False :
                print("目录不存在,创建中...........创建完成")
                os.makedirs(os.path.join(self.data.get('path')))

            with open(fullname, 'w') as fp:
                fp.write(content)

            print("{fullname} craete ....... [successful!]".format(fullname=fullname))
            return
        else:
            print("参数不完整")
            return

    def get_path(self):
        '''
        获取用户存放文章的 PATH,主要通过 读取当前目录下的 pelicanconfig.py
        来查询 PATH 变量
        若 pelicanconfig.py 文件不存在或者其中不包含 PATH 变量,并且命令行参数中没有指定 PATH,
        则返回 None
        '''
        pelicanconfig = 'pelicanconfig.py'
        pelicanconfig_path = os.path.join(os.getcwd(), pelicanconfig)

        if os.path.exists(pelicanconfig_path):            # 读取文件内容,查找 PATH 变量
            with open(pelicanconfig, 'r') as fp:
                path = re.search('[^#]PATH\s*=\s*(.*)', fp.read()) # 注释的 PATH 不提取
                return path.group(1).replace('\'', '') if path else ''
        else:
            return ''

    def translation(self, query, from_ = 'auto', to = 'en'):
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
        content = argv[2] + '\n' + (len(argv[2])+2)*'=' + \
                '\n:date: '+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + \
                '\n:slug: ' + replace(translation(argv[2])) + \
                '\n:modified: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + \
                '\n:author: ' + AUTHOR

        ext = '.rst' if type_ == 'resTructured' else '.md'
        with open(PATH+'/'+filename+ext, 'w') as fp:
            fp.write(content)

def replace(string):
    '''
    将空格转换成 -
    '''
    return string.replace(' ', '-')

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
    # main()
    autotool = Autotool(sys.argv)
    # autotool.read_pelicanconfig()
    print(autotool.data)
    autotool.get_path()
    autotool.run()
    # print(autotool.data)
