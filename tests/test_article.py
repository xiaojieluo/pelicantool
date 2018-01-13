import pytest
from pelicantool.parser import ParserFactory
from pelicantool.article import Article
import os
import shutil


def test_article_handle_duplicate_name():
    article = Article({})
    path = 'tests/article'
    full_path = article.handle_duplicate_name(path, 'test.txt')
    assert full_path == 'tests/article/test.txt'

    with open(os.path.join(path, 'test.txt'), 'w+') as fp:
        fp.write('')

    full_path = article.handle_duplicate_name(path, 'test.txt')
    assert full_path == 'tests/article/test.1.txt'

    os.remove('tests/article/test.txt')

def test_article__create_file():
    article = Article({})
    path = 'tests/tmp/text.txt'
    article._create_file(path, 'hello')
    assert os.path.exists(path) is True

    with open(path, 'r') as fp:
        assert  fp.read() == 'hello'

    # 清理测试文件
    os.remove(path)
    os.rmdir(os.path.dirname(path))

@pytest.fixture(params = ['hello', None])
def data(request):
    return {
        'title': '标题',
        'tags': request.param,
        'slug': 'Title',
        'author': 'Xiaojie Luo',
        'date': '2018-01-10 19:01:35',
        'modified': '2018-01-10 19:01:35',
        'file_name': '2018-01-10-标题',
        }

def test_article__content(data):
    article = Article({})

    content = get_content(data)

    assert content == article._content(data)

def get_content(data):
    content = list()
    content.append('Title: ' + data['title'])
    content.append('Date: ' + data['date'])
    content.append('Modified: ' + data['modified'])
    content.append('Slug: ' + data['slug'])
    if data.get('tags', None):
        content.append('Tags: ' + data['tags'])
    content.append('Author: ' + data['author'])
    content.append(len(data['slug']) * 5 * '-')
    content.append('\n')

    content = '\n'.join(content)
    return content

def test_article_create(data):
    path = './tmp'

    article = Article({
        'config_dir': 'tests',
        'Article':{
            'floder': path
        }
    })

    article.create(data)

    with open(os.path.join('tests/tmp', data['file_name']+'.md'), 'r') as fp:
        assert fp.read() == get_content(data)

    os.remove(os.path.join('tests/tmp', data['file_name']+'.md'))
    os.rmdir('tests/tmp')
