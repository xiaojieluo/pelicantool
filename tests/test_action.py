import pytest
from pelicantool.article import ActionInterface
from pelicantool.exceptions import InterfaceNotImplete

class TT(ActionInterface):
    pass


def test_action_interface():
    tt = TT({})
    with pytest.raises(InterfaceNotImplete):
        tt.run()

def test_action_getattr():
    tt = TT({})
    tt.test = 'hello'

    assert tt.test == 'hello'
