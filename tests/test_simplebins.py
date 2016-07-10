import reprlib

from binpackp import SimpleBin, VolumeError
import pytest


@pytest.fixture()
def abin(request):
    a = SimpleBin(10)
    return a


@pytest.fixture()
def bbin(request):
    b = SimpleBin(5)
    return b


@pytest.fixture()
def items(request):
    i = ["abc", "123"]
    return i


@pytest.fixture()
def aitems(request, items):
    ai = SimpleBin(10)
    ai._items = list(items)
    items_size = sum([len(x) for x in list(items)])
    ai._available_volume = 10 - items_size
    return ai


def test_init(abin, bbin):
    assert (abin._volume == 10 and bbin._volume == 5)
    assert (abin._available_volume == 10 and bbin._volume == 5)
    assert (abin._items == [] and bbin._items == [])


def test_available_volume_getter(abin, bbin):
    assert (abin.available_volume == 10 and bbin.available_volume == 5)


def test_volume_getter(abin, bbin):
    assert (abin.volume == 10 and bbin.volume == 5)


def test_volume_setter(abin, aitems):
    abin.volume = 5
    assert (abin.volume == 5)
    with pytest.raises(ValueError):
        abin.volume = -1
    with pytest.raises(ValueError):
        abin.volume = 0
    with pytest.raises(VolumeError):
        aitems.volume = 1


def test__bool__(abin, aitems):
    assert (not bool(abin))
    assert (bool(aitems))


def test__contains__(abin, items, aitems):
    assert (items[0] not in abin)
    assert (items[0] in aitems)


def test__hash__(abin):
    name = "SimpleBin"
    volume = 10
    items = []
    assert (hash(abin.__class__.__name__) == hash(name))
    assert (hash(abin._volume) == hash(volume))
    assert (hash(tuple(abin._items)) == hash(tuple(items)))
    assert (hash(abin) == hash(name) ^ hash(volume) ^ hash(tuple(items)))
    assert (not hash(abin) == hash(bbin))


def test__eq__(abin, bbin, items, aitems):
    assert (abin == SimpleBin(10) and bbin == SimpleBin(5))
    assert (not abin == bbin)
    bbin._items = items
    assert (not aitems == bbin)
    cbin = SimpleBin(10)
    cbin._items = ["abc", "12"]
    assert (not aitems == cbin)
    cbin._items = items
    assert (aitems == cbin)
    assert (not abin == tuple(items))
    assert (abin != [])


def test__getitem__(abin, items, aitems):
    with pytest.raises(IndexError):
        abin.__getitem__(0)
    assert (aitems.__getitem__(0) == items[0])


def test__iter__(abin, items, aitems):
    assert (list(iter(abin)) == list(iter([])))
    assert (not list(iter(abin)) == list(iter(items)))
    assert (list(iter(aitems)) == list(iter(items)))


def test__len__(abin, items, aitems):
    assert (len(abin) == 0)
    assert (not len(abin) == len(items))
    assert (len(aitems) == len(items))


def test__repr__(abin, items, aitems):
    rpr_str = "<SimpleBin>(Volume: {}/{}, Items: {})"
    assert (abin.__repr__() == rpr_str.format(0, 10, []))
    assert (aitems.__repr__() == rpr_str.format(6, 10, reprlib.repr(items)))


def test__reversed__(items, aitems):
    assert (items == aitems._items)
    items = list(items.__reversed__())
    assert (not items == aitems._items)
    aitems._items = list(aitems.__reversed__())
    assert (items == aitems._items)


def test_size(items):
    assert (len(items[0]) == SimpleBin.size(items[0]))


def test__delitem__(abin, items, aitems):
    with pytest.raises(IndexError):
        del abin[0]
    av = aitems._available_volume
    assert (aitems._items == items)
    del aitems[0]
    assert (aitems._items == items[1:] and aitems._available_volume == av + len(items[0]))


def test__setitem__(abin, items, aitems):
    with pytest.raises(IndexError):
        abin.__setitem__(0, items[0])
    with pytest.raises(VolumeError):
        aitems.__setitem__(0, items[0] * 4)
    ov = aitems._available_volume
    aitems.__setitem__(0, items[1])
    assert (aitems[0] == items[1] and aitems._available_volume == ov)
    aitems.__setitem__(0, items[0] * 2)
    assert (aitems[0] == items[0] * 2 and aitems._available_volume == ov - len(items[0]))
    aitems.__setitem__(0, items[0])
    assert (aitems[0] == items[0] and aitems._available_volume == ov)


def test_fits(abin, items):
    assert (abin._fits(items[0]) == len(items[0]))
    with pytest.raises(VolumeError):
        abin._fits(items[0] * 4)


def test_append(abin, items):
    abin.append(items[0])

    assert (abin._items == items[:1] and abin._available_volume == abin._volume - len(items[0]))
    with pytest.raises(VolumeError):
        abin.append(items[0] * 4)


def test_clear(aitems, abin):
    aitems.clear()
    assert (aitems == abin)


def test_count(abin, aitems, items):
    assert (abin.count(items[0]) == 0)
    assert (aitems.count(items[0]) == items.count(items[0]))


def test_extend(abin, items):
    abin.extend(items)
    assert (abin._items == items and abin._available_volume == 10 - 6)
    with pytest.raises(VolumeError):
        abin.extend(items)


def test_insert(abin, items):
    abin.insert(0, items[0])
    assert (abin._items == items[:1] and abin._available_volume == 10 - len(items[0]))
    with pytest.raises(VolumeError):
        abin.insert(1, items[0] * 4)


def test_remove(aitems, items):
    assert (items[0] in aitems)
    aitems.remove(items[0])
    assert (items[0] not in aitems and aitems._available_volume == 10 - len(aitems._items[0]))


def test_reverse(aitems, items):
    aitems.reverse()
    items.reverse()
    assert (aitems._items == items)
