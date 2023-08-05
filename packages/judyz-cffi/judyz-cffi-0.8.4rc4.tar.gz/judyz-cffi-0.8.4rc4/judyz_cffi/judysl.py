from typing import TYPE_CHECKING

from six import PY3, text_type

from .exceptions import JudyError
from .internal import _cjudy, _ffi, _load

if TYPE_CHECKING:
    from typing import Iterable, Mapping, Optional, Tuple, Union


__all__ = ["JudySL", "JudySLIterator"]

_load()


class StringCache(object):
    MAX_BUILDER_SIZE = 360
    buf = None

    @staticmethod
    def acquire(capacity):
        """Acquire a buffer of a particular size.

        If we've got one in cache, returns it.
        """
        if capacity <= StringCache.MAX_BUILDER_SIZE:
            b = StringCache.buf
            if b is not None:
                if capacity <= len(b):
                    StringCache.buf = None
                    b[0] = 0
                    return b
        return _ffi.new("unsigned char[%d]" % capacity)

    @staticmethod
    def release(buf):
        """Release the buffer.

        It must not be used thereafter.
        """
        if len(buf) <= StringCache.MAX_BUILDER_SIZE:
            StringCache.buf = buf


class JudySLIterator(object):
    _STATE_FIRST = 0
    _STATE_NEXT = 1
    _STATE_END = 2

    def __init__(self, j):
        # type: (JudySL) -> None
        self._j = j
        self._array = j._array  # noqa
        self._state = JudySLIterator._STATE_FIRST
        self._index = StringCache.acquire(j._max_len)  # noqa

    def __iter__(self):
        return self

    def next(self):
        # type: () -> Tuple[str, int]
        err = _ffi.new("JError_t *")
        if self._state == JudySLIterator._STATE_FIRST:
            p = _cjudy.JudySLFirst(self._array[0], self._index, err)
            self._state = JudySLIterator._STATE_NEXT
        elif self._state == JudySLIterator._STATE_NEXT:
            p = _cjudy.JudySLNext(self._array[0], self._index, err)
        else:
            raise StopIteration()
        if p == _ffi.NULL:
            StringCache.release(self._index)
            self._state = JudySLIterator._STATE_END
            raise StopIteration()
        if p == JudySL.M1:
            raise JudyError(err.je_Errno)
        v = _ffi.cast("signed long", p[0])
        k = _ffi.string(self._index)
        if PY3:
            k = k.decode("utf-8")
        return k, int(v)

    __next__ = next


class JudySL(object):
    """
    JudySL class.
    """

    M1 = _ffi.cast("void*", -1)

    def __init__(self, other=None):
        # type: (Optional[Union[Mapping[str, int], Iterable[Tuple[str, int]]]]) -> None
        self._array = _ffi.new("JudySL **")
        self._max_len = 1
        if other:
            self.update(other)

    def update(self, other):
        # type: (Optional[Union[Mapping[str, int], Iterable[Tuple[str, int]]]]) -> None
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
        err = _ffi.new("JError_t *")
        if _cjudy.JudySLFreeArray(self._array, err) == -1:
            raise JudyError(err.je_Errno)

    def __len__(self):
        n = 0
        for k, v in self.iteritems():
            n += 1
        return n

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()

    def __setitem__(self, key, value):
        # type: (str, int) -> None
        err = _ffi.new("JError_t *")
        if isinstance(key, text_type):
            key = key.encode("utf-8")
        p = _cjudy.JudySLIns(self._array, key, err)
        if p == _ffi.NULL:
            raise JudyError(err.je_Errno)
        p[0] = _ffi.cast("void*", value)
        klen = len(key) + 1
        if self._max_len < klen:
            self._max_len = klen

    def inc(self, key):
        # type: (str) -> None
        err = _ffi.new("JError_t *")
        if isinstance(key, text_type):
            key = key.encode("utf-8")
        p = _cjudy.JudySLIns(self._array, key, err)
        if p == _ffi.NULL:
            raise JudyError(err.je_Errno)
        p[0] = _ffi.cast("void*", int(_ffi.cast("long", p[0])) + 1)
        klen = len(key) + 1
        if self._max_len < klen:
            self._max_len = klen

    def __getitem__(self, item):
        # type: (str) -> int
        err = _ffi.new("JError_t *")
        if isinstance(item, text_type):
            item = item.encode("utf-8")
        p = _cjudy.JudySLGet(self._array[0], item, err)
        if p == _ffi.NULL:
            raise KeyError(item)
        if p == JudySL.M1:
            raise JudyError(err.je_Errno)
        return int(_ffi.cast("signed long", p[0]))

    def __contains__(self, item):
        # type: (str) -> bool
        err = _ffi.new("JError_t *")
        if isinstance(item, text_type):
            item = item.encode("utf-8")
        p = _cjudy.JudySLGet(self._array[0], item, err)
        if p == JudySL.M1:
            raise JudyError(err.je_Errno)
        return p != _ffi.NULL

    def get(self, item, default_value=0):
        # type: (str, int) -> int
        err = _ffi.new("JError_t *")
        if isinstance(item, text_type):
            item = item.encode("utf-8")
        p = _cjudy.JudySLGet(self._array[0], item, err)
        if p == _ffi.NULL:
            return default_value
        if p == JudySL.M1:
            raise JudyError(err.je_Errno)
        return int(_ffi.cast("signed long", p[0]))

    def __iter__(self):
        return JudySLIterator(self)

    def items(self):
        # type: () -> Iterable[Tuple[str, int]]
        err = _ffi.new("JError_t *")
        index = StringCache.acquire(
            self._max_len
        )  # _ffi.new("char[%d]" % self._max_len)
        try:
            p = _cjudy.JudySLFirst(self._array[0], index, err)
            if p == JudySL.M1:
                raise Exception("err={}".format(err.je_Errno))
            if p == _ffi.NULL:
                return
            v = int(_ffi.cast("signed long", p[0]))
            k = _ffi.string(index)
            if PY3:
                k = k.decode("utf-8")
            yield k, v
            while True:
                p = _cjudy.JudySLNext(self._array[0], index, err)
                if p == JudySL.M1:
                    raise Exception("err={}".format(err.je_Errno))
                if p == _ffi.NULL:
                    break
                v = int(_ffi.cast("signed long", p[0]))
                k = _ffi.string(index)
                if PY3:
                    k = k.decode("utf-8")
                yield k, v
        finally:
            StringCache.release(index)

    iteritems = items

    def keys(self):
        for k, v in self.items():
            yield k

    iterkeys = keys

    def values(self):
        # type: () -> Iterable[str]
        for k, v in self.items():
            yield v

    itervalues = values

    def get_first(self, buf=None):
        """
        Get the first item in the JudySL
        :param buf: None...
        :return: (key, value, internal "iterator" for get_next) or (None, None, None)
        :rtype: tuple
        """
        err = _ffi.new("JError_t *")
        if buf is None:
            buf = StringCache.acquire(self._max_len)
        p = _cjudy.JudySLFirst(self._array[0], buf, err)
        if p == JudySL.M1:
            StringCache.release(buf)
            raise Exception("err={}".format(err.je_Errno))
        if p == _ffi.NULL:
            StringCache.release(buf)
            return None, None, None
        v = int(_ffi.cast("signed long", p[0]))
        k = _ffi.string(buf)
        if PY3:
            k = k.decode("utf-8")
        return k, v, buf

    def get_next(self, buf):
        """
        Get the next item in the JudySL
        :param buf: internal "iterator" returned by get_first or get_next
        :type buf:
        :return: (key, value, internal "iterator" for get_next) or (None, None, None)
        :rtype: tuple
        """
        if buf is None:
            return None, None, None
        err = _ffi.new("JError_t *")
        p = _cjudy.JudySLNext(self._array[0], buf, err)
        if p == JudySL.M1:
            StringCache.release(buf)
            raise Exception("err={}".format(err.je_Errno))
        if p == _ffi.NULL:
            StringCache.release(buf)
            return None, None, None
        v = int(_ffi.cast("signed long", p[0]))
        k = _ffi.string(buf)
        if PY3:
            k = k.decode("utf-8")
        return k, v, buf
