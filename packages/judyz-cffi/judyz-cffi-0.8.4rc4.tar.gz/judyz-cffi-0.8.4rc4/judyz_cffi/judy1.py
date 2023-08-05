from typing import TYPE_CHECKING

from .exceptions import JudyError
from .internal import _cjudy, _ffi, _load

if TYPE_CHECKING:
    from typing import Iterable, Optional

__all__ = ["Judy1", "Judy1Iterator"]

_load()


class Judy1Iterator(object):
    def __init__(self, j):
        # type: (Judy1) -> None
        self._j = j
        self._array = j._array  # noqa
        self._start = True
        self._index = _ffi.new("signed long*")

    def __iter__(self):
        return self

    def next(self):
        # type: () -> int
        err = _ffi.new("JError_t *")
        if self._start:
            rc = _cjudy.Judy1First(self._array[0], self._index, err)
            self._start = False
        else:
            rc = _cjudy.Judy1Next(self._array[0], self._index, err)
        if rc == 0:
            raise StopIteration()
        if rc == -1:
            raise JudyError(err.je_Errno)
        return self._index[0]

    __next__ = next


class Judy1(object):
    """
    Judy1 class.
    """

    def __init__(self, iterable=None):
        # type: (Optional[Iterable[int]]) -> None
        self._array = _ffi.new("Judy1 **")
        if iterable:
            for item in iterable:
                self.add(item)

    def add(self, item):
        # type: (int) -> None
        err = _ffi.new("JError_t *")
        if _cjudy.Judy1Set(self._array, item, err) == -1:
            raise JudyError(err.je_Errno)

    def clear(self):
        # type: () -> None
        err = _ffi.new("JError_t *")
        if _cjudy.Judy1FreeArray(self._array, err) == -1:
            raise JudyError(err.je_Errno)

    def _get(self, item):
        # type: (int) -> bool
        err = _ffi.new("JError_t *")
        rc = _cjudy.Judy1Test(self._array[0], item, err)
        if rc == -1:
            raise JudyError(err.je_Errno)
        return rc

    def __contains__(self, item):
        # type: (int) -> bool
        return self._get(item)

    def __len__(self):
        # type: () -> int
        err = _ffi.new("JError_t *")
        rc = _cjudy.Judy1Count(self._array[0], 0, -1, err)
        if rc == -1:
            raise JudyError(err.je_Errno)
        return rc

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()

    def discard(self, item):
        # type: (int) -> None
        err = _ffi.new("JError_t *")
        rc = _cjudy.Judy1Unset(self._array, item, err)
        if rc == -1:
            raise JudyError(err.je_Errno)

    def remove(self, item):
        # type: (int) -> None
        err = _ffi.new("JError_t *")
        rc = _cjudy.Judy1Unset(self._array, item, err)
        if rc == 0:
            raise KeyError(item)
        if rc == -1:
            raise JudyError(err.je_Errno)

    def __iter__(self):
        return Judy1Iterator(self)
