from typing import TYPE_CHECKING

from .exceptions import JudyError
from .internal import _cjudy, _ffi, _load

if TYPE_CHECKING:
    from typing import Iterable, Mapping, Optional, Tuple, Union

__all__ = ["JudyL", "JudyLIterator"]

_load()


class JudyLIterator(object):
    def __init__(self, j):
        # type: (JudyL) -> None
        self._j = j
        self._array = j._array  # noqa
        self._start = True
        self._index = _ffi.new("signed long*")

    def __iter__(self):
        return self

    def next(self):
        # type: () -> Tuple[int, int]
        err = _ffi.new("JError_t *")
        if self._start:
            p = _cjudy.JudyLFirst(self._array[0], self._index, err)
            self._start = False
        else:
            p = _cjudy.JudyLNext(self._array[0], self._index, err)
        if p == _ffi.NULL:
            raise StopIteration()
        if p == JudyL.M1:
            raise JudyError(err.je_Errno)
        v = _ffi.cast("signed long", p[0])
        return self._index[0], int(v)

    __next__ = next


class JudyL(object):
    """
    JudyL class.
    """

    M1 = _ffi.cast("void*", -1)

    def __init__(self, other=None):
        self._array = _ffi.new("JudyL **")
        if other:
            self.update(other)

    def update(self, other):
        # type: (Optional[Union[Mapping[int, int], Iterable[Tuple[int, int]]]]) -> None
        if other is None:
            return
        has_keys = True
        try:
            other.keys  # noqa
        except AttributeError:
            has_keys = False
        if has_keys:
            for key in other:
                self[key] = other[key]
        else:
            for (k, v) in other:
                self[k] = v

    def clear(self):
        # type: () -> None
        err = _ffi.new("JError_t *")
        if _cjudy.JudyLFreeArray(self._array, err) == -1:
            raise JudyError(err.je_Errno)

    def __len__(self):
        # type: () -> int
        err = _ffi.new("JError_t *")
        rc = _cjudy.JudyLCount(self._array[0], 0, -1, err)
        if rc == -1:
            raise JudyError(err.je_Errno)
        return rc

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()

    def __setitem__(self, key, value):
        # type: (int, int) -> None
        err = _ffi.new("JError_t *")
        p = _cjudy.JudyLIns(self._array, key, err)
        if p == _ffi.NULL:
            raise JudyError(err.je_Errno)
        p[0] = _ffi.cast("void*", value)

    def __getitem__(self, item):
        # type: (int) -> int
        err = _ffi.new("JError_t *")
        p = _cjudy.JudyLGet(self._array[0], item, err)
        if p == _ffi.NULL:
            raise KeyError(item)
        if p == JudyL.M1:
            raise JudyError(err.je_Errno)
        return int(_ffi.cast("signed long", p[0]))

    def __contains__(self, item):
        # type: (int) -> bool
        err = _ffi.new("JError_t *")
        p = _cjudy.JudyLGet(self._array[0], item, err)
        if p == JudyL.M1:
            raise JudyError(err.je_Errno)
        return p != _ffi.NULL

    def get(self, item, default_value=0):
        # type: (int, int) -> int
        err = _ffi.new("JError_t *")
        p = _cjudy.JudyLGet(self._array[0], item, err)
        if p == _ffi.NULL:
            return default_value
        if p == JudyL.M1:
            raise JudyError(err.je_Errno)
        return int(_ffi.cast("signed long", p[0]))

    def inc(self, key, value=1):
        # type: (int, int) -> None
        err = _ffi.new("JError_t *")
        p = _cjudy.JudyLIns(self._array, key, err)
        if p == _ffi.NULL:
            raise JudyError(err.je_Errno)
        p[0] = int(_ffi.cast("signed long", p[0])) + _ffi.cast("void*", value)

    def __iter__(self):
        return JudyLIterator(self)

    def items(self):
        # type: () -> Iterable[Tuple[int, int]]
        err = _ffi.new("JError_t *")
        index = _ffi.new("signed long*")
        p = _cjudy.JudyLFirst(self._array[0], index, err)
        if p == JudyL.M1:
            raise Exception("err={}".format(err.je_Errno))
        if p == _ffi.NULL:
            return
        v = int(_ffi.cast("signed long", p[0]))
        yield index[0], v
        while 1:
            p = _cjudy.JudyLNext(self._array[0], index, err)
            if p == JudyL.M1:
                raise Exception("err={}".format(err.je_Errno))
            if p == _ffi.NULL:
                break
            v = int(_ffi.cast("signed long", p[0]))
            yield index[0], v

    iteritems = items

    def keys(self):
        # type: () -> Iterable[int]
        err = _ffi.new("JError_t *")
        index = _ffi.new("signed long*")
        p = _cjudy.JudyLFirst(self._array[0], index, err)
        if p == JudyL.M1:
            raise Exception("err={}".format(err.je_Errno))
        if p == _ffi.NULL:
            return
        yield index[0]
        while 1:
            p = _cjudy.JudyLNext(self._array[0], index, err)
            if p == JudyL.M1:
                raise Exception("err={}".format(err.je_Errno))
            if p == _ffi.NULL:
                break
            yield index[0]

    iterkeys = keys
