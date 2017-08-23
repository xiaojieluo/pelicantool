from pelicantool.pelicantool import Article
# import pelicantool.pelicantool
import pytest
import os
import datetime

class TestPelicantool(object):

    def setup_class(self):
        self.article = Article()


    def test_article_author(self):

        assert self.article.author == 'Xiaojie Luo'

    def test_article_tags(self):
        pass

    def test_article_create(self):
        self.article.title = '测试标题'
        self.article.create()

        assert os.path.isfile(os.path.join('content',self.article.filename)) is True



def test_article_create():
    article = Article()
    assert article.author == 'Xiaojie Luo'
    return True

# if __name__ == '__main__':
#     import sys

    # print(os.getcwd())
