from binpackp import Fit, SimpleBin, NumberBin, BinOrdering
import pytest


@pytest.fixture()
def nums(request):
    return [9, 5, 6, 8, 7, 3, 1]


@pytest.fixture()
def chars(request, nums):
    return ["A" * n for n in nums]


@pytest.fixture()
def bin_size(request):
    return 10


def bin_sorter(bin_to_sort):
    return sorted(bin_to_sort, key=lambda x: hash(x))


def test_def_sbin(chars, bin_size):
    inputs = chars
    bin_cls = SimpleBin
    a = Fit.fit(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[0].append(inputs[6])
    expected[1].append(inputs[1])
    expected[1].append(inputs[5])
    expected[2].append(inputs[2])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    assert(bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_def_nbin(nums, bin_size):
    inputs = nums
    bin_cls = NumberBin
    a = Fit.fit(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[0].append(inputs[6])
    expected[1].append(inputs[1])
    expected[1].append(inputs[5])
    expected[2].append(inputs[2])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_vol_sbin(chars):
    inputs = chars
    bin_cls = SimpleBin
    a = Fit.fit(bin_cls, 9, inputs)
    expected = [bin_cls(9) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[1].append(inputs[1])
    expected[1].append(inputs[5])
    expected[1].append(inputs[6])
    expected[2].append(inputs[2])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_vol_nbin(nums):
    inputs = nums
    bin_cls = NumberBin
    a = Fit.fit(bin_cls, 9, inputs)
    expected = [bin_cls(9) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[1].append(inputs[1])
    expected[1].append(inputs[5])
    expected[1].append(inputs[6])
    expected[2].append(inputs[2])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_sort_rev_sbin(chars, bin_size):
    inputs = chars
    bin_cls = SimpleBin
    a = Fit.fit(bin_cls, bin_size, inputs, sort=True)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[0].append(inputs[6])
    expected[1].append(inputs[3])
    expected[2].append(inputs[4])
    expected[2].append(inputs[5])
    expected[3].append(inputs[2])
    expected[4].append(inputs[1])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_sort_rev_nbin(nums, bin_size):
    inputs = nums
    bin_cls = NumberBin
    a = Fit.fit(bin_cls, bin_size, inputs, sort=True)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[0].append(inputs[6])
    expected[1].append(inputs[3])
    expected[2].append(inputs[4])
    expected[2].append(inputs[5])
    expected[3].append(inputs[2])
    expected[4].append(inputs[1])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_sort_sbin(chars, bin_size):
    inputs = chars
    bin_cls = SimpleBin
    a = Fit.fit(bin_cls, bin_size, inputs, sort=True, sort_reversed=False)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[6])
    expected[0].append(inputs[5])
    expected[0].append(inputs[1])
    expected[1].append(inputs[2])
    expected[2].append(inputs[4])
    expected[3].append(inputs[3])
    expected[4].append(inputs[0])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_sort_nbin(nums, bin_size):
    inputs = nums
    bin_cls = NumberBin
    a = Fit.fit(bin_cls, bin_size, inputs, sort=True, sort_reversed=False)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[6])
    expected[0].append(inputs[5])
    expected[0].append(inputs[1])
    expected[1].append(inputs[2])
    expected[2].append(inputs[4])
    expected[3].append(inputs[3])
    expected[4].append(inputs[0])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_start(bin_size):
    a = Fit.fit(SimpleBin, bin_size, [], starting_bins=2)
    assert (a.bins == tuple([SimpleBin(bin_size), SimpleBin(bin_size)]))


def test_start_bins_lt_one(bin_size):
    a = Fit.fit(SimpleBin, bin_size, [], starting_bins=-1)
    assert (a.bins == tuple([SimpleBin(bin_size)]))


def test_max_bin_sbin(chars, bin_size):
    inputs = chars
    bin_cls = SimpleBin
    a = Fit.fit(bin_cls, bin_size, inputs, max_open_bins=2)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[1].append(inputs[1])
    expected[1].append(inputs[5])
    expected[1].append(inputs[6])
    expected[2].append(inputs[2])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_max_bin_nbin(nums, bin_size):
    inputs = nums
    bin_cls = NumberBin
    a = Fit.fit(bin_cls, bin_size, inputs, max_open_bins=2)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[1].append(inputs[1])
    expected[1].append(inputs[5])
    expected[1].append(inputs[6])
    expected[2].append(inputs[2])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_meth_name(bin_size):
    bin_cls = SimpleBin
    a = Fit.fit(bin_cls, bin_size, [], method_name="TESTING")
    assert (a.method == "TESTING")


def test_bin_order_best_sbin(chars, bin_size):
    inputs = chars
    bin_cls = SimpleBin
    a = Fit.fit(bin_cls, bin_size, inputs, bin_sort=BinOrdering.best_fit)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[0].append(inputs[6])
    expected[1].append(inputs[1])
    expected[2].append(inputs[2])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    expected[4].append(inputs[5])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_bin_order_best_nbin(nums, bin_size):
    inputs = nums
    bin_cls = NumberBin
    a = Fit.fit(bin_cls, bin_size, inputs, bin_sort=BinOrdering.best_fit)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[0].append(inputs[6])
    expected[1].append(inputs[1])
    expected[2].append(inputs[2])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    expected[4].append(inputs[5])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_bin_order_worst_sbin(chars, bin_size):
    inputs = chars
    bin_cls = SimpleBin
    a = Fit.fit(bin_cls, bin_size, inputs, bin_sort=BinOrdering.worst_fit)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[1].append(inputs[1])
    expected[1].append(inputs[5])
    expected[2].append(inputs[2])
    expected[2].append(inputs[6])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_bin_order_worst_nbin(nums, bin_size):
    inputs = nums
    bin_cls = NumberBin
    a = Fit.fit(bin_cls, bin_size, inputs, bin_sort=BinOrdering.worst_fit)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[1].append(inputs[1])
    expected[1].append(inputs[5])
    expected[2].append(inputs[2])
    expected[2].append(inputs[6])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_ff_sbin(chars, bin_size):
    inputs = chars
    bin_cls = SimpleBin
    a = Fit.ff(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[0].append(inputs[6])
    expected[1].append(inputs[1])
    expected[1].append(inputs[5])
    expected[2].append(inputs[2])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)) and a.method == "First Fit (FF)")


def test_ff_nbin(nums, bin_size):
    inputs = nums
    bin_cls = NumberBin
    a = Fit.ff(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[0].append(inputs[6])
    expected[1].append(inputs[1])
    expected[1].append(inputs[5])
    expected[2].append(inputs[2])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)) and a.method == "First Fit (FF)")


def test_ffd_sbin(chars, bin_size):
    inputs = chars
    bin_cls = SimpleBin
    a = Fit.ffd(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[0].append(inputs[6])
    expected[1].append(inputs[3])
    expected[2].append(inputs[4])
    expected[2].append(inputs[5])
    expected[3].append(inputs[2])
    expected[4].append(inputs[1])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)) and a.method == "First Fit Decreasing (FFD)")


def test_ffd_nbin(nums, bin_size):
    inputs = nums
    bin_cls = NumberBin
    a = Fit.ffd(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[0].append(inputs[6])
    expected[1].append(inputs[3])
    expected[2].append(inputs[4])
    expected[2].append(inputs[5])
    expected[3].append(inputs[2])
    expected[4].append(inputs[1])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)) and a.method == "First Fit Decreasing (FFD)")


def test_nf_sbin(chars, bin_size):
    inputs = chars
    bin_cls = SimpleBin
    a = Fit.nf(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(6)]
    expected[0].append(inputs[0])
    expected[1].append(inputs[1])
    expected[2].append(inputs[2])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    expected[4].append(inputs[5])
    expected[5].append(inputs[6])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)) and a.method == "Next Fit (NF)")


def test_nf_nbin(nums, bin_size):
    inputs = nums
    bin_cls = NumberBin
    a = Fit.nf(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(6)]
    expected[0].append(inputs[0])
    expected[1].append(inputs[1])
    expected[2].append(inputs[2])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    expected[4].append(inputs[5])
    expected[5].append(inputs[6])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)) and a.method == "Next Fit (NF)")


def test_bf_sbin(chars, bin_size):
    inputs = chars
    bin_cls = SimpleBin
    a = Fit.bf(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[0].append(inputs[6])
    expected[1].append(inputs[1])
    expected[2].append(inputs[2])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    expected[4].append(inputs[5])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_bf_nbin(nums, bin_size):
    inputs = nums
    bin_cls = NumberBin
    a = Fit.bf(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[0].append(inputs[6])
    expected[1].append(inputs[1])
    expected[2].append(inputs[2])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    expected[4].append(inputs[5])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_bfd_sbin(chars, bin_size):
    inputs = chars
    bin_cls = SimpleBin
    a = Fit.bfd(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[0].append(inputs[6])
    expected[1].append(inputs[3])
    expected[2].append(inputs[4])
    expected[2].append(inputs[5])
    expected[3].append(inputs[2])
    expected[4].append(inputs[1])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_bfd_nbin(nums, bin_size):
    inputs = nums
    bin_cls = NumberBin
    a = Fit.bfd(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[0].append(inputs[6])
    expected[1].append(inputs[3])
    expected[2].append(inputs[4])
    expected[2].append(inputs[5])
    expected[3].append(inputs[2])
    expected[4].append(inputs[1])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_wf_sbin(chars, bin_size):
    inputs = chars
    bin_cls = SimpleBin
    a = Fit.wf(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[1].append(inputs[1])
    expected[1].append(inputs[5])
    expected[2].append(inputs[2])
    expected[2].append(inputs[6])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_wf_nbin(nums, bin_size):
    inputs = nums
    bin_cls = NumberBin
    a = Fit.wf(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[1].append(inputs[1])
    expected[1].append(inputs[5])
    expected[2].append(inputs[2])
    expected[2].append(inputs[6])
    expected[3].append(inputs[3])
    expected[4].append(inputs[4])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_wfd_sbin(chars, bin_size):
    inputs = chars
    bin_cls = SimpleBin
    a = Fit.wfd(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[1].append(inputs[3])
    expected[2].append(inputs[4])
    expected[3].append(inputs[2])
    expected[3].append(inputs[6])
    expected[4].append(inputs[1])
    expected[4].append(inputs[5])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_wfd_nbin(nums, bin_size):
    inputs = nums
    bin_cls = NumberBin
    a = Fit.wfd(bin_cls, bin_size, inputs)
    expected = [bin_cls(bin_size) for _ in range(5)]
    expected[0].append(inputs[0])
    expected[1].append(inputs[3])
    expected[2].append(inputs[4])
    expected[3].append(inputs[2])
    expected[3].append(inputs[6])
    expected[4].append(inputs[1])
    expected[4].append(inputs[5])
    assert (bin_sorter(a.bins) == bin_sorter(tuple(expected)))


def test_replace_blank():
    assert (Fit._replace_method_code(None) == "Custom")


def test_detect_method_variant():
    assert (Fit._detect_method(False, False, 1, BinOrdering.best_fit, None) == Fit._replace_method_code("bfv"))


def test_starting_bins_gt_max_bins(bin_size):
    inputs = []
    bin_cls = SimpleBin
    a = Fit.fit(bin_cls, bin_size, inputs, starting_bins=10, max_open_bins=3)
    assert (a.total_bins == 3)
