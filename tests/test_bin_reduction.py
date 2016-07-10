from binpackp import SimpleBin, NumberBin
from binpackp.fit import BinReduction
import pytest


@pytest.fixture()
def items(request):
    nitems = [8, 9, 8]
    sitems = ["A" * x for x in nitems]
    return nitems, sitems


@pytest.fixture()
def sbin(request, items):
    _, sitems = items
    sbins = [SimpleBin(10) for _ in range(3)]
    bins = []
    for abin, val in zip(sbins, sitems):
        abin.append(val)
        bins.append(abin)
    return bins


@pytest.fixture()
def nbin(request, items):
    nitems, _ = items
    nbins = [NumberBin(10) for _ in range(3)]
    bins = []
    for abin, val in zip(nbins, nitems):
        abin.append(val)
        bins.append(abin)
    return bins


def test_min_volume_sbin(sbin):
    the_bin = sbin
    assert(BinReduction.min_volume(the_bin) == the_bin[1])


def test_min_volume_nbin(nbin):
    the_bin = nbin
    assert(BinReduction.min_volume(the_bin) == the_bin[1])


def test_first_sbin(sbin):
    the_bin = sbin
    assert(BinReduction.first(the_bin) == the_bin[0])


def test_first_nbin(nbin):
    the_bin = nbin
    assert(BinReduction.first(the_bin) == the_bin[0])
