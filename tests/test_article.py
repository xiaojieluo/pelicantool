import pytest
from pelicantool import pelicantool
from pelicantool import ParserFactory
import os
from pelicantool.article import Article

def test_article_create():
    # Done.
    parser = ParserFactory.factory(['create', 'article', '-c=tests/'])
    action = parser.instance()

    data = {
        'title': '标题',
        'tags': 'hello, world',
        'slug': 'Title',
        'author': 'Xiaojie Luo',
        'date': '2018-01-10 19:01:35',
        'modified': '2018-01-10 19:01:35',
        'file_name': '2018-01-10-标题',
    }
    action.create(data)

    path = 'tests/content/2018-01-10-标题.md'
    assert os.path.exists(path) == True
    # 清理测试文件
    os.remove(path)

# def test_parse_articles_config():
#     parser = ParserFactory.factory(['create', 'article'])
#     action = parser.instance()
#
#     print(action.run())
#     print(action.args)


def test_article_handle_duplicate_name():
    # Done.
    article = Article(None)

    path = 'tests/text'
    filename = 'test.txt'
    full_path = article.handle_duplicate_name(path, filename)
    with open(full_path, 'w+') as fp:
        fp.write('')
    assert os.path.exists('tests/text/test.txt') is True

    full_path = article.handle_duplicate_name(path, filename)
    with open(full_path, 'w+') as fp:
        fp.write('')
    assert os.path.exists('tests/text/test.1.txt') is True

def test_article__create():
    # Done.
    article = Article({})
    full_path = article.handle_duplicate_name('tests/no_config', 'test.txt')

    article._create_file(full_path, 'hello, text')
    with open(full_path) as fp:
        assert fp.read() == 'hello, text'

    # 清理测试文件
    os.remove(full_path)
