import pytest
from pelicantool.parser import ParserFactory, ArgsParser
from pelicantool.article import Article

def test_parser_instance():
    parser = ParserFactory.factory(['create', 'article'])
    action = parser.instance()
    assert type(action) == Article

def test_parser_args_and_default_toml_args():
    parser = ParserFactory.factory(['create', 'article', '-c=tests/'])
    action = parser.instance()
    assert action.args['config_dir'] == 'tests/'
    assert action.args['Article']['floder'] == './content'

    parser = ParserFactory.factory(['create', 'article'])
    action = parser.instance()
    assert action.args['Article']['author'] == ''
