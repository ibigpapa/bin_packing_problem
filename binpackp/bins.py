"""Generic bins"""

import numbers
import reprlib


class VolumeError(Exception):
    pass


class SimpleBin(object):
    """An object to represent a bin in the Bin Packing Problem."""

    def __init__(self, volume):
        self._volume = 0
        self._available_volume = 0
        self.volume = volume
        self._items = []

    @property
    def available_volume(self):
        return self._available_volume

    @property
    def items(self):
        return self._items

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        if value < 1:
            raise ValueError("Volume must be a value greater than 0.  ({} <= 0)".format(value))
        required_vol = self._volume - self._available_volume
        if value < required_vol:
            msg = "Existing items have a total size of {} which is larger than desired volume of {}."
            raise VolumeError(msg.format(required_vol, value))
        self._volume = value
        self._available_volume = value - required_vol

    def __bool__(self):
        return bool(self._items)

    def __contains__(self, item):
        return self._items.__contains__(item)

    def __delitem__(self, key):
        frees = self.size(self._items[key])
        self._items.__delitem__(key)
        self._available_volume += frees

    def __eq__(self, other):
        try:
            return hash(self) == hash(other)
        except TypeError:
            return False

    def __getitem__(self, item):
        return self._items.__getitem__(item)

    def __hash__(self):
        return hash(self.__class__.__name__) ^ hash(self._volume) ^ hash(tuple(self.items))

    def __iter__(self):
        return self._items.__iter__()

    def __len__(self):
        return self._items.__len__()

    def __repr__(self):
        return "<{}>(Volume: {}/{}, Items: {})".format(self.__class__.__name__, self._volume - self._available_volume,
                                                       self._volume, reprlib.repr(self._items))

    def __reversed__(self):
        return self._items.__reversed__()

    def __setitem__(self, key, value):
        required = self.size(value)
        replacing_size = self.size(self[key])
        diff = replacing_size - required
        if self._available_volume + diff < 0:
            msg = "Item of size {} that is replacing item of size {} would exceed volume {}."
            raise VolumeError(msg.format(required, replacing_size, self._volume))
        self._items.__setitem__(key, value)
        self._available_volume += diff

    def append(self, p_object):
        required = self._fits(p_object)
        self._items.append(p_object)
        self._available_volume -= required

    def clear(self):
        self._items.clear()
        self._available_volume = self._volume

    def count(self, value):
        return self._items.count(value)

    def extend(self, iterable):
        required = sum([self.size(i) for i in iterable])
        if required > self._available_volume:
            msg = "Items of total size {} is unable to fit in available volume {}."
            raise VolumeError(msg.format(required, self._available_volume))
        self._items.extend(iterable)
        self._available_volume -= required

    def insert(self, index, p_object):
        required = self._fits(p_object)
        self._items.insert(index, p_object)
        self._available_volume -= required

    def remove(self, value):
        self._items.remove(value)
        self._available_volume += self.size(value)

    def reverse(self):
        self._items.reverse()

    def _fits(self, value):
        required = self.size(value)
        if required > self._available_volume:
            raise VolumeError("Item of size {} is unable to fit in available volume {}.".format(required,
                                                                                                self._available_volume))
        return required

    @staticmethod
    def size(value):
        """Provides the capacity requirement of the item given.

        Args:
            value: The value can be any item supporting the Len function call.

        Returns:
            Integer representing the length of the value.
        """
        return len(value)


class NumberBin(SimpleBin):
    @staticmethod
    def size(value):
        if not isinstance(value, numbers.Number):
            raise TypeError("Value is of type {}, expected to see type of Number".format(type(value)))
        return value
