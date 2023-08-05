import copy
import numpy as np
import matplotlib.pyplot as plt
import collections

from .time_index import TimeIndex
from .utils import is_scalar
from .options import options


format_float = "%." + str(options["precision"]) + "f"

def format_number(number):
    if isinstance(number, float):
        return format_float % number
    else:
        return str(number)


class Vector:
    """Represents an n-dimensional vector.

    Attributes:
      values (list-like): The values in the vector.
    """

    def __init__(self, values):
        self.values = tuple(values)

    def __getitem__(self, n):
        return self.values[n]

    def __call__(self, n):
        return self.__getitem__(n)

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        if len(self.values) > options["max_elements"]:
            values = [format_number(v) for v in
                      self.values[:(options["max_elements"] - 1)]]
            return ("(" +
                    ", ".join(values) +
                    ", ..., " +
                    format_number(self.values[-1]) +
                    ")")
        else:
            values = [format_number(v) for v in self.values]
            return ("(" +
                    ", ".join(values) +
                    ")")

    def __len__(self):
        return len(self.values)

    
class InfiniteVector:
    """Represents an infinite vector.

    The elements of the infinite vector are evaluated lazily
    and are memoized.

    Attributes:
      fun: A function that takes in an index n and the 
           curret vector and returns the value at n.
    """

    def __init__(self, fun):
        self.fun = fun
        self.values = {}

    def __getitem__(self, n):
        # special case to handle slices
        if isinstance(n, slice):
            # if no upper bound, return InfiniteVector
            if n.stop is None:
                n0 = 0 if n.start is None else n.start
                k = 1 if n.step is None else n.step
                if k < 0:
                    raise KeyError(
                        "It is not possible to index an "
                        "InfiniteVector backwards."
                    )
                def f(m, vector):
                    return self[n0 + k * m]
                return InfiniteVector(f)
            # otherwise, return Vector
            else:
                return Vector(
                    self[m] for m in range(*n.indices(n.stop))
                )

        # check if value has been calculated already
        if n in self.values:
            return self.values[n]
        else:
            if n < 0 or not isinstance(n, int):
                raise KeyError(
                    "The index of an InfiniteVector "
                    "must be a non-negative integer."
                )
            val = self.fun(n, self)
            self.values[n] = val
            return val

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        values = [format_number(self[v])
                  for v in range(options["max_elements"])]
        return ("(" +
                ", ".join(values) +
                ", ...)")
    
    
class TimeFunction:

    def __init__(self, fun, timeIndex):
        self.fun = fun
        self.timeIndex = timeIndex

    def __getitem__(self, t):
        return self.fun(t)

    def __call__(self, t):
        return self.fun(t)

    def __str__(self):
        if self.timeIndex.fs == float("inf"):
            return "(continuous-time function)"
        else:
            return str(tuple([self.fun(self.timeIndex[n]) for n in range(10)] + ["..."]))

    def plot(self, *args, **kwargs):
        axes = plt.gca()
        tmin, tmax = axes.get_xlim()
        if self.timeIndex.fs == float("inf"):
            ts = np.linspace(tmin, tmax, 200)
        else:
            nmin = int(np.floor(tmin * self.timeIndex.fs))
            nmax = int(np.ceil(tmax * self.timeIndex.fs))
            ts = [self.timeIndex[n] for n in range(nmin, nmax + 1)]
        y = [self[t] for t in ts]
        plt.plot(ts, y, *args, **kwargs)

    def _operation_factory(self, op):
        def op_fun(self, other):
            if is_scalar(other):
                return TimeFunction(lambda t: op(self[t], other), self.timeIndex)
            elif isinstance(other, TimeFunction):
                self.timeIndex.check_same(other.timeIndex)
                return TimeFunction(lambda t: op(self[t], other[t]), self.timeIndex)
            else:
                return NotImplemented

        return op_fun

    def __add__(self, other):
        op_fun = self._operation_factory(lambda x, y: x + y)
        return op_fun(self, other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        op_fun = self._operation_factory(lambda x, y: x - y)
        return op_fun(self, other)

    def __rsub__(self, other):
        return -1 * self.__sub__(other)

    def __neg__(self):
        return -1 * self

    def __mul__(self, other):
        op_fun = self._operation_factory(lambda x, y: x * y)
        return op_fun(self, other)
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        op_fun = self._operation_factory(lambda x, y: x / y)
        return op_fun(self, other)

    def __rtruediv__(self, other):
        op_fun = self._operation_factory(lambda x, y: y / x)
        return op_fun(self, other)

    def __pow__(self, other):
        op_fun = self._operation_factory(lambda x, y: x ** y)
        return op_fun(self, other)

    def __rpow__(self, other):
        op_fun = self._operation_factory(lambda x, y: y ** x)
        return op_fun(self, other)

