import os
import sys
import subprocess
import time
import random
import hashlib
import urllib.parse
import requests
import re
import yaml
import argparse
import six

__version__ = '0.1.0'
PATH = 'content'
type_ = 'resTructured'  # Markdown
# FILENAME = '%Y-%m-%d-{title}'
FILENAME = '{time}-{title}'
AUTHOR = 'xiaojieluo'


if six.PY3:
    str_compat = str
else:
    str_compat = unicode


def ask(question, answer=str_compat, default=None, l=None):
    if answer == str_compat:
        r = ''
        while True:
            if default:
                r = _input_compat('> {0} [{1}] '.format(question, default))
            else:
                r = _input_compat('> {0} '.format(question, default))

            r = r.strip()

            if len(r) <= 0:
                if default:
                    r = default
                    break
                else:
                    print('You must enter something')
            else:
                if l and len(r) != l:
                    print('You must enter a {0} letters long string'.format(l))
                else:
                    break

        return r

    elif answer == bool:
        r = None
        while True:
            if default is True:
                r = _input_compat('> {0} (Y/n) '.format(question))
            elif default is False:
                r = _input_compat('> {0} (y/N) '.format(question))
            else:
                r = _input_compat('> {0} (y/n) '.format(question))

            r = r.strip().lower()

            if r in ('y', 'yes'):
                r = True
                break
            elif r in ('n', 'no'):
                r = False
                break
            elif not r:
                r = default
                break
            else:
                print("You must answer 'yes' or 'no'")
        return r
    elif answer == int:
        r = None
        while True:
            if default:
                r = _input_compat('> {0} [{1}] '.format(question, default))
            else:
                r = _input_compat('> {0} '.format(question))

            r = r.strip()

            if not r:
                r = default
                break

            try:
                r = int(r)
                break
            except:
                print('You must enter an integer')
        return r
    else:
        raise NotImplemented(
            'Argument `answer` must be str_compat, bool, or integer')


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
            'title': '',
            'date': time.strftime('%Y-%m-%d', time.localtime()),
            'time': time.strftime('%H:%M:%S', time.localtime()),
            'author': '',
            'type': 'rst',
            'summary': '',
            'author': 'xiaojieluo',
            'tags': '',
            'slug': '',
            'filename': '{date}-{title}',
            'path': self.get_path(),
        }
        self.content = list()

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
            self.show_help()  # 显示帮助信息之后退出程序
            return
        if '-author' in self.argv:
            self._get_para(self.argv.index('-author'), 'author')
        if '-date' in self.argv:
            self._get_para(self.argv.index('-date'), 'date')
        if '-path' in self.argv:
            self._get_para(self.argv.index('-path'), 'path')
        if '-type' in self.argv:
            self._get_para(self.argv.index('-type'), 'type')
        if '-time' in self.argv:
            self._get_para(self.argv.index('-time'), 'time')
        if '-tags' in self.argv:
            self._get_para(self.argv.index('-tags'), 'tags')

        if 'create' in self.argv:
            self._get_para(self.argv.index('create'), 'title')
            if len(self.argv) > self.argv.index('create') + 1:
                self.create(self.argv)

            return

    def _get_para(self, index, name):
        '''
        内部函数,将解析出来的参数保存到 self.data 字典中
        '''
        if len(self.argv) > index + 1:
            self.data[name] = self.argv[index + 1]
        else:
            print("参数不完整")

    def create(self, argv):
        '''
        创建指定的文章
        '''

        if self.data.get('title'):
            # if self.data.get('date') == '':
            #     self.data['date'] = time.strftime('%Y-%m-%d', time.localtime());

            filename = FILENAME.format(
                time=self.data['date'], title=self.data['title'])

            self.content.append(self.data['title'])
            self.content.append(len(self.data['title']) * '==' + '\n')
            self.content.append(
                ':date: ' + self.data['date'] + ' ' + self.data['time'])
            self.content.append(
                ':modified: ' + self.data['date'] + ' ' + self.data['time'])
            self.content.append(
                ':slug: ' + self.replace(self.translation(self.data['title'])))
            if self.data.get('tags'):
                self.content.append(':tags: ' + self.data['tags'])
            self.content.append(':author: ' + self.data['author'])
            self.content.append('\n')

            ext = '.rst' if (self.data.get('type') == (
                'rst' or 'resTructured')) else '.md'
            fullname = os.path.join(self.data.get('path'), filename) + ext

            if self._create_file(fullname, '\n'.join(self.content)):
                print("{fullname} craete ....... [successful!]".format(
                    fullname=fullname))
            else:
                print("failed!")
        else:
            print("参数不完整")
            return

    def _create_file(self, fullname, content):
        # 目录不存在,则创建
        if os.path.isdir(os.path.join('./', self.data.get('path'))) is False:
            print("目录不存在,创建中...........创建完成")
            os.makedirs(os.path.join(self.data.get('path')))

        with open(fullname, 'w') as fp:
            fp.write(content)

        return True

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
                path = re.search('[^#]PATH\s*=\s*(.*)',
                                 fp.read())  # 注释的 PATH 不提取
                return path.group(1).replace('\'', '') if path else ''
        else:
            return ''

    def translation(self, query, from_='zh', to='en'):
        '''
        请求百度翻译 api 获取翻译结果
        '''
        appid = '20161217000034172'
        secretKey = '07Qh2zEwKIx3kGwer1Uz'
        salt = random.randint(32768, 65536)
        sign = appid + query + str(salt) + secretKey
        m1 = hashlib.md5(sign.encode('utf8'))
        sign = m1.hexdigest()
        url = 'http://api.fanyi.baidu.com/api/trans/vip/translate?'
        url = url + urllib.parse.urlencode(
            {'q': query, 'from': from_, 'to': to, 'appid': appid, 'salt': salt, 'sign': sign})

        r = requests.get(url)
        r.encoding = 'utf-8'
        result = r.json()
        print(result)
        if 'error_code' in result:
            # raise TransLationError
            return None

        if 'trans_result' in result:
            return result['trans_result'][0].get('dst', None)

        return None

    def replace(self, string):
        '''
        将空格转换成 -
        '''
        return string.replace(' ', '-')


sys.path.append(os.getcwd())
import pelicanconf

class Pelican(object):

    def __init__(self):
        self.conf = pelicanconf
        # try:
        #     import pelicanconf
        # except ModuleNotFoundError as e:
        #     print(e)

    @property
    def author(self):
        '''作者信息'''

        return self.conf.AUTHOR

    @property
    def sitename(self):
        return self.conf.SITENAME


def main():
    parser = argparse.ArgumentParser(
        prog='pelican_tool',
        description='A auto tool for Pelican',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    parser.add_argument('--foo', action='store_true')
    parser.add_argument('--append', action='append')
    args = parser.parse_args()

    print('''Welcome to pelican-quickstart v{v}.

This script will help you create a new Pelican-based website.

Please answer the following questions so this script can generate the files
needed by Pelican.

    '''.format(v=__version__))
    print(args)
    pelican = Pelican()
    print(pelican.author)
    # autotool = Autotool(sys.argv)
    # autotool.get_path()
    # autotool.run()


if __name__ == '__main__':
    main()
