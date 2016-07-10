from binpackp import SimpleBin, Fit
from binpackp.fit import BPResult
import pytest


@pytest.fixture()
def basic(request):
    return Fit.ffd(SimpleBin, 5, "a ab d c w xx z".split())


def test_total_bins(basic):
    assert (basic.total_bins == 2)


def test_unused_volume(basic):
    assert (basic.unused_volume == 1)


def test_used_volume(basic):
    assert (basic.used_volume == 9)


def test_total_volume(basic):
    assert (basic.total_volume == 10)


def test_unused_percent(basic):
    assert (basic.unused_percent == (1 / 10) * 100)


def test_used_percent(basic):
    assert (basic.used_percent == (9/10) * 100)


def test_items(basic):
    items = "a ab d c w xx z".split()
    assert (basic.items == items)
    nb = BPResult(basic.bins)
    assert (sorted(nb.items) == sorted(items))


def test_total_items(basic):
    items = "a ab d c w xx z".split()
    assert (basic.total_items == len(items))
    nb = BPResult(basic.bins)
    assert (nb.total_items == len(items))


def test_repr():
    a = Fit.fit(SimpleBin,1,[])
    assert(a.__repr__() == "<BPResult (Total Bins: 1, Total Volume: 1, Unused Volume: 1)>")
