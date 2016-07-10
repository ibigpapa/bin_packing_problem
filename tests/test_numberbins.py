
from binpackp import NumberBin
import pytest


def test_size():
    assert(NumberBin.size(1) == 1 and NumberBin.size(3) == 3)
    with pytest.raises(TypeError):
        NumberBin.size('a')
