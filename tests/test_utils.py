# @pytest.fixture(params)
import pytest
from pelicantool.utils import translation, ask, str_compat

def test_utils_translation():
    zh_string = "标题"

    assert translation(zh_string) == 'Title'
