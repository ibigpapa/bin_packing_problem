from .bins import VolumeError


class BinOrdering(object):

    @classmethod
    def none(cls, bins):
        """Does nothing to existing order.

        Args:
            bins:           A list of bins.

        Returns:
            The bins argument as is.
        """
        return bins

    @classmethod
    def best_fit(cls, bins):
        """Sorts a list of bins with smallest available volume first.

        Args:
            bins:           A list of bins.

        Returns:
            A list of bins sorted with smallest available volume first.
        """
        return sorted(bins, key=lambda x: x.available_volume)

    @classmethod
    def worst_fit(cls, bins):
        """Sorts a list of bins with largest available volume first.

        Args:
            bins:           A list of bins.

        Returns:
            A list of bins sorted with largest available volume first.
        """
        return sorted(bins, key=lambda x: x.available_volume, reverse=True)

    first_fit = none
    next_fit = none


class BinReduction(object):
    @classmethod
    def min_volume(cls, bins):
        """ Finds the bin with the smallest available volume.

            Args:
                bins:   A list of bins.

            Returns:
                First bin with the smallest available volume from list.
        """
        return min(bins, key=lambda x: x.available_volume)

    @classmethod
    def first(cls, bins):
        """ Gets the first bin.

        Args:
            bins:   A list of bins.

        Returns:
            First bin from list.
        """
        return bins[0]

    first_fit = min_volume
    next_fit = first


class Fit(object):
    @classmethod
    def fit(cls, bin_cls, bin_volume, items, sort=False, sort_reversed=True, starting_bins=1, max_open_bins=0,
            bin_sort=BinOrdering.none, bin_reduction=BinReduction.min_volume, method_name=None,
            method_detection=True):
        """Performs the first/next/best/worst fit algorithms and variant's.

        Args:
            bin_cls:            The class of bin to use.
            bin_volume:         The volume of each bin.
            items:              The items to be packed.
            sort:               Sort items before packing by size.  Defaults to False.
            sort_reversed:      If sort is true will sort items by size in reverse.  Defaults to True.
            starting_bins:      Positive number of bins to create before packing begins. A value < 1 is assumed to be 1.
                                If > max_open_bins the value is reduce to max_open_bins. Default is 1.
            max_open_bins:      The number of bins to keep in the list of bins to be considered during packing.
                                An value < 1 indicates no limit.  If value is >=1 then when the number of open bins
                                exceeds the max_open_bins the bin reduction method is used to close a bin.
                                Default is 0(no limit).
            bin_sort:       The BinOrdering class method to use when ordering the bins after insertion.
                                Defaults to none method.
            bin_reduction:      The BinReduction class method to use when max_open_bins is reached.
                                Defaults to min_volume method.
            method_name:        Descriptive name for parameters used. Defaults to None.
            method_detection:   If method name is None will attempt to add name based on argument values.
                                Default is True.

        Returns:
            A Bin Packing Result object.
        """
        if method_name is None and method_detection:
            method_name = cls._detect_method(sort, sort_reversed, max_open_bins, bin_sort, bin_reduction)
        if starting_bins < 1:
            starting_bins = 1
        if starting_bins > max_open_bins != 0:
            starting_bins = max_open_bins
        open_bins = [bin_cls(bin_volume) for _ in range(starting_bins)]
        closed_bins = []
        the_items = [item for item in iter(items)]
        if sort:
            the_items.sort(reverse=sort_reversed, key=lambda x: bin_cls.size(x))
        for item in the_items:
            open_bins_len = len(open_bins)
            counter = 0
            packed = False
            bin_full = -1
            if bin_cls.size(item) == bin_volume:
                closed_bins.append(bin_cls(bin_volume))
                closed_bins[-1].append(item)
                continue
            while counter < open_bins_len:
                try:
                    open_bins[counter].append(item)
                    packed = True
                    if open_bins[counter].available_volume == 0:
                        closed_bins.append(open_bins.pop(counter))
                    break
                except VolumeError:
                    counter += 1
            if not packed:
                open_bins.append(bin_cls(bin_volume))
                open_bins[-1].append(item)
                if 1 <= max_open_bins < len(open_bins):
                    bin_to_reduce = bin_reduction(open_bins)
                    closed_bins.append(bin_to_reduce)
                    bin_full = open_bins.index(bin_to_reduce)
            if bin_full > -1:
                del open_bins[bin_full]
            open_bins = bin_sort(open_bins)
        return BPResult(closed_bins + open_bins, items, method_name=method_name)

    @classmethod
    def ff(cls, bin_cls, bin_volume, items):
        """Wrapper for parameters required to provided classic first fit algorithm."""
        return cls.fit(bin_cls, bin_volume, items)

    @classmethod
    def ffd(cls, bin_cls, bin_volume, items):
        """Wrapper for parameters required to provide classic first fit Descending algorithm."""
        return cls.fit(bin_cls, bin_volume, items, sort=True)

    @classmethod
    def nf(cls, bin_cls, bin_volume, items):
        """Wrapper for parameters required to provide classic next fit algorithm."""
        return cls.fit(bin_cls, bin_volume, items, max_open_bins=1, bin_reduction=BinReduction.first)

    @classmethod
    def bf(cls, bin_cls, bin_volume, items):
        """Wrapper for parameters required to provide classic best fit algorithm."""
        return cls.fit(bin_cls, bin_volume, items, bin_sort=BinOrdering.best_fit)

    @classmethod
    def bfd(cls, bin_cls, bin_volume, items):
        """Convenience function providing Best Fit Decreasing BF algorithm variation"""
        return cls.fit(bin_cls, bin_volume, items, sort=True, bin_sort=BinOrdering.best_fit)

    @classmethod
    def wf(cls, bin_cls, bin_volume, items):
        """Wrapper for parameters required to provide classic worst fit algorithm."""
        return cls.fit(bin_cls, bin_volume, items, bin_sort=BinOrdering.worst_fit)

    @classmethod
    def wfd(cls, bin_cls, bin_volume, items):
        """Convenience function providing worst Fit Decreasing wf algorithm variation"""
        return cls.fit(bin_cls, bin_volume, items, sort=True, bin_sort=BinOrdering.worst_fit)

    @classmethod
    def _detect_method(cls, sort, sort_reversed, max_open_bins, bin_ordering, bin_reduction):
        code = "cv"
        if bin_ordering == BinOrdering.best_fit:
            code = "bf"
        if bin_ordering == BinOrdering.worst_fit:
            code = "wf"
        if bin_ordering == BinOrdering.none:
            if bin_reduction == BinReduction.min_volume:
                code = "Ff"
            if bin_reduction == BinReduction.first:
                code = "Nf"
        if sort and sort_reversed:
            code += "d"
        if max_open_bins > 0 or (sort and not sort_reversed):
            if code != "cv" and (code != "Nf" and max_open_bins == 1):
                code += "v"
        return cls._replace_method_code(code)

    @staticmethod
    def _replace_method_code(code):
        if not code:
            return "Custom"
        codes = {"b": "Best",
                 "w": "Worst",
                 "f": "Fit",
                 "F": "First",
                 "N": "Next",
                 "c": "Custom",
                 "d": "Decreasing",
                 "v": "Variant"}
        return " ".join([codes[c] for c in code]) + " ({})".format(code.upper())


class BPResult(object):
    def __init__(self, bins, items=None, method_name=None):
        r_bins = tuple(bins)
        self._cache = {"bins": r_bins, "method_name": method_name, "total_bins": len(r_bins)}
        if items is not None:
            self._cache["items"] = items
            self._cache["total_items"] = len(items)

    @property
    def method(self):
        return self._cache["method_name"]

    @property
    def bins(self):
        return self._cache["bins"]

    @property
    def total_bins(self):
        return self._cache["total_bins"]

    @property
    def unused_volume(self):
        if "unused" not in self._cache:
            self._cache["unused"] = sum([ben.available_volume for ben in self.bins])
        return self._cache["unused"]

    @property
    def used_volume(self):
        if "used" not in self._cache:
            self._cache["used"] = self.total_volume - self.unused_volume
        return self._cache["used"]

    @property
    def total_volume(self):
        if "total" not in self._cache:
            self._cache["total"] = sum([ben.volume for ben in self.bins])
        return self._cache["total"]

    @property
    def unused_percent(self):
        if "unused_per" not in self._cache:
            self._cache["unused_per"] = (self.unused_volume / self.total_volume) * 100
        return self._cache["unused_per"]

    @property
    def used_percent(self):
        if "used_per" not in self._cache:
            self._cache["used_per"] = (self.used_volume / self.total_volume) * 100
        return self._cache["used_per"]

    @property
    def items(self):
        if "items" not in self._cache:
            items = []
            for ben in self.bins:
                items += ben.items
            self._cache["items"] = items
        return self._cache["items"]

    @property
    def total_items(self):
        if "total_items" not in self._cache:
            self._cache["total_items"] = len(self.items)
        return self._cache["total_items"]

    def __repr__(self):
        return "<BPResult (Total Bins: {}, Total Volume: {}, Unused Volume: {})>".format(self.total_bins,
                                                                                         self.total_volume,
                                                                                         self.unused_volume
                                                                                         )